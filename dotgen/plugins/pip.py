# -*- coding: utf-8 -*-
from dotgen.process import watch_process

rank = 3

def handle(output_dir, config):
    return
    for package in config:
        watch_process(["pip", "install", "--upgrade", "--user", package])
