import sys
import subprocess
import os
import atexit

class Phantom(object):
    def __init__(self):
        self.proc = subprocess.Popen(["phantom-plot", "--multiple-files"], stdin=subprocess.PIPE, stdout = subprocess.PIPE, bufsize=0)

    def __del__(self):
        self.kill()

    def kill(self):
        try:
            self.proc.stdin.write(b"exit\n")
            self.proc.wait()
        except:
            pass

    def process(self, inf, outf):
        if not self.proc:
            raise ValueError("phantomjs not launched")
        self.proc.stdin.write((os.path.realpath(inf) + " " + os.path.realpath(outf) + "\n").encode())
        x = self.proc.stdout.readline().decode("utf-8")
        if x != "ok\n":
            raise ValueError(x)

phantom = Phantom()

def cleanup():
    if phantom:
        phantom.kill()

atexit.register(cleanup)

def plot_file(inf, outf):
    return phantom.process(inf, outf)


def main():
    while True:
        try:
            [inf, outf] = input().split(" ")
        except:
            break
        phantom.process(inf, outf)


if __name__ == "__main__":
    main()
