# -*- coding: utf-8 -*-

import os
import json
import copy
import subprocess

USAGE = """
hhdpy tex_to_img_url
"""

def to_img_url(args):
    math = args[0]
    math = math.replace("+", "%2B")
    math = math.replace("σ", "\\sigma")
    url = "https://render.githubusercontent.com/render/math?math={}".format(math)
    print(url)
