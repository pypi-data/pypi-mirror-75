"""Main module."""

import os
import subprocess as sp
from time import sleep
import re
import json
import sys
import click
import signal

_PID_FILE = "jupyter.pid"
_JUPYTER_LOG = "jupyter.log"
_JMANAGER_LOG = "jmanager.log"


def receiveSignal(signalNumber, frame):
    if not os.path.isfile(_PID_FILE):
        return
    with open(_PID_FILE) as f:
        pid = json.load(f)
    with open(_JMANAGER_LOG) as f:
        f.write(f"receiving signal {signalNumber}. removing {_PID_FILE}. it's contents was {json.dumps(pid)}")
    os.remove(_PID_FILE)


class Launcher:
    def __init__(self):
        pass

    def __del__(self):
        os.remove(_PID_FILE)

    def launch(self):
        with open(_JUPYTER_LOG, "w") as f:
            po = sp.Popen(["jupyter", "lab"],
                          stdout=f,
                          stderr=sp.STDOUT,
                          text=True)
        sleep(5)
        with open(_JUPYTER_LOG) as f:
            for l in f:
                r = re.match(r"^ +http://localhost:([0-9]+)/\?token=([0-9a-z]+)$", l)
                if r:
                    port, token = r.expand(r"\1"), r.expand(r"\2")
        with open(_PID_FILE, "w") as f:
            dat = dict(
                pid=po.pid,
                port=int(port),
                token=token
            )
            json.dump(dat, f)
        signal.signal(signal.SIGTERM, receiveSignal)
        po.wait()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        run()


@main.command(help="Terminate jupyter process")
def kill():
    if os.path.exists(_PID_FILE):
        with open(_PID_FILE) as f:
            pid = json.load(f)
        sp.Popen(["kill", "-9", str(pid["pid"])])


def open_browser():
    with open(_PID_FILE) as f:
        dat = json.load(f)
    url = f"http://localhost:{dat['port']}/?token={dat['token']}"
    sys.stderr.write(json.dumps(dat) + "\n")
    sys.stderr.write(url + "\n")
    sp.Popen(["open", url])


@main.command(hidden=True)
def launch():
    launcher = Launcher()
    launcher.launch()


@main.command(help="Launch new jupyter or connect to existing one.")
def run():
    if not os.path.exists(_PID_FILE):
        sys.stderr.write("launching new jupyter process\n")
        sp.Popen(["jmanager", "launch"])
    else:
        sys.stderr.write("jupyter process already run\n")
        open_browser()


@main.command(help="Print lines for .gitignore")
def ignore():
    print(_PID_FILE)
    print(_JUPYTER_LOG)
    print(_JMANAGER_LOG)
