# -*- coding: utf-8 -*-

import os
import json
import copy
import subprocess

USAGE = """
hhdpy jupyter_py_to_ipynb
    --skip-if-existed
"""

IPYNB_JSON = """
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0 ",
      "1 ",
      "2 ",
      "3 ",
      "4 "
     ]
    }
   ],
   "source": [
    "for i in range(0, 5) : ",
    "    print(i)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# head ",
    "## head2 ",
    "### head3 "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.17"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""


def py_to_ipynb(args):
    skip_if_existed = False

    if len(args) > 0 and args[0] == "--skip-if-existed":
        skip_if_existed = True

    j_ipynb = json.loads(IPYNB_JSON)
    j_code = j_ipynb["cells"][0]
    j_md = j_ipynb["cells"][1]
    j_md["source"] = []
    j_code["source"] = []
    j_code["outputs"] = []
    j_ipynb["cells"] = []
    cwd = os.getcwd()

    for fileName in os.listdir(cwd):
        if fileName.endswith(".py"):
            pyFullFilePath = os.path.join(cwd, fileName)
            ipynbFullPath = os.path.join(cwd, fileName.replace(".py", ".ipynb"))

            if os.path.exists(ipynbFullPath) and skip_if_existed == True :
                print("{} already existed ... skip!!!".format(ipynbFullPath))
                continue

            pyFile = open(pyFullFilePath, "r", encoding="utf-8")
            j_ipynb_new = copy.deepcopy(j_ipynb)
            curType = "none"  # code, md
            print("{} start ...".format(pyFullFilePath))

            while True:
                line = pyFile.readline()

                if not line:
                    break

                if line.strip().startswith("#" * 10):
                    if curType != "md":
                        j_md_new = copy.deepcopy(j_md)
                        j_ipynb_new["cells"].append(j_md_new)
                    curType = "md"
                elif not line.strip().startswith("#"):
                    if curType != "code":
                        j_code_new = copy.deepcopy(j_code)
                        j_ipynb_new["cells"].append(j_code_new)
                    curType = "code"

                if curType == "md":
                    if line.strip().startswith("#"):
                        if line.strip().startswith("#" * 10):
                            j_md_new["source"].append("--- \n")
                        else:
                            j_md_new["source"].append("{} \n".format(line.strip().strip("#")))
                elif curType == "code":
                    j_code_new["source"].append(line)

            pyFile.close()

            ipynbFile = open(ipynbFullPath, "w", encoding="utf-8")
            jsonStr = json.dumps(j_ipynb_new, indent=4, ensure_ascii=False)
            ipynbFile.write(jsonStr)
            ipynbFile.close()
            print("{} finish !!!".format(ipynbFullPath))

            try:
                cmd = "jupyter nbconvert --to notebook --execute {} --inplace --ExecutePreprocessor.timeout=86400".format(ipynbFullPath)
                print("cmd[{}]".format(cmd))
                res = subprocess.check_output(cmd, shell=True).decode("utf-8")
                print("res[{}]".format(res))
            except:
                print("except!!! cmd[{}]".format(cmd))