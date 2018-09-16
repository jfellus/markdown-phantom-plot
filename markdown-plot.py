import sys
import subprocess
import os

class Phantom(object):
    def __init__(self):
        self.proc = subprocess.Popen(["phantom-plot", "--multiple-files"], stdin=subprocess.PIPE)

    def __del__(self):
        if self.proc:
            self.proc.terminate()

    def process(self, inf, outf):
        if not self.proc:
            raise ValueError("phantomjs not launched")
        self.proc.stdin.write((os.path.realpath(inf) + " " + os.path.realpath(outf) + "\n").encode())

phantom = Phantom()


def markdown_plot_file(inf, outf):
    return phantom.process(inf, outf)

def main():
    while True:
        try:
            [inf, outf] = input().split(" ")
        except:
            break
        phantom.process(inf, outf)
        print("Processed " + inf + " -> " + outf)


if __name__ == "__main__":
    main()
