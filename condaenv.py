#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import hashlib
import urllib
import argparse
from collections import defaultdict
from snakemake.workflow import Workflow
from snakemake.dag import DAG

parser = argparse.ArgumentParser(
    """
Parse snakemake workflow and retrieve conda environment files.
"""
)
parser.add_argument(
    "--wrapper-prefix",
    metavar="wrapper_prefix",
    type=str,
    help="wrapper prefix",
    default=None
)
parser.add_argument(
    "--snakefile",
    metavar="snakefile",
    type=str,
    help="snakefile",
    default="Snakefile"
)

args = parser.parse_args()
wrapper_prefix = args.wrapper_prefix
snakefile = args.snakefile

if wrapper_prefix is not None:
    wrapper_prefix=f"file:{wrapper_prefix}"
rootdir = os.path.abspath(os.path.dirname(snakefile))

wf = Workflow(snakefile=snakefile, wrapper_prefix=wrapper_prefix)
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
            contents = "".join(fh.readlines()).strip()
    md5hash.update(contents.encode())
    envs[md5hash.hexdigest()] = contents

md5hash = hashlib.md5()
for k, v in envs.items():
    md5hash.update(v.encode())
    print(v)
