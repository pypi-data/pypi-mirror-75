# -*- coding: utf-8 -*-

import sys
import hhdpy.typora
import hhdpy.jupyter
import hhdpy.tex

USAGE = ""
USAGE += hhdpy.typora.USAGE
USAGE += hhdpy.jupyter.USAGE
USAGE += hhdpy.tex.USAGE


def main():
    if len(sys.argv) < 2:
        print("\nUSAGE : {}".format(USAGE))
        exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "typora_new_file":
        hhdpy.typora.new_file(args)
    elif cmd == "jupyter_py_to_ipynb":
        hhdpy.jupyter.py_to_ipynb(args)
    elif cmd == "tex_to_img_url":
        hhdpy.tex.to_img_url(args)
    else:
        print("\n'{}' is unknown command!!!\nUSAGE : {}".format(cmd, USAGE))

if __name__ == "__main__":
    sys.exit(main())
