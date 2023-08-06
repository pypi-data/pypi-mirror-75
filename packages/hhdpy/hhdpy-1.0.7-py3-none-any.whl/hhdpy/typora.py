# -*- coding: utf-8 -*-

import os
import datetime

USAGE = """
hhdpy typora_new_file "실험결과 최종보고서"
hhdpy typora_github_io_article_step1 "200101 실험결과 최종보고서.md"
hhdpy typora_github_io_article_step2 "2020-01-01-실험결과-최종보고서.md" 
"""

def new_file(args):
    title = args[0]
    yymmdd = datetime.datetime.now().strftime("%y%m%d")
    filePath = os.path.join(os.getcwd(), "{} {}.md".format(yymmdd, title))
    file = open(filePath, "w", encoding="utf-8", newline="")
    file.write("# {} {}\n".format(yymmdd, title))
    file.close()
