#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import hashlib
import urllib
from collections import defaultdict
from snakemake.workflow import Workflow
from snakemake.dag import DAG

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
snakefile = os.path.join(os.path.join(rootdir, "Snakefile"))
# wrapper_prefix = os.path.join(rootdir, "workflow", "wrappers")

wf = Workflow(snakefile=snakefile) # , wrapper_prefix=f"file:{wrapper_prefix}")
wf.include(snakefile, overwrite_first_rule=True)
wf.check()

envs = defaultdict(dict)

for rule in wf.rules:
    md5hash = hashlib.md5()
    if rule.conda_env is None:
        continue
    fn = re.sub(r"^file:", "", rule.conda_env)
    if fn.startswith("http"):
        response = urllib.request.urlopen(fn)
        contents = "".join(response.read().decode())
    else:
        with open(fn, "r") as fh:
            contents = "".join(fh.readlines())
    md5hash.update(contents.encode())
    envs[md5hash.hexdigest()] = contents

md5hash = hashlib.md5()
for k, v in envs.items():
    md5hash.update(v.encode())
print(md5hash.hexdigest())
