# -*- coding: utf-8 -*-
from dotgen.process import watch_process

rank = 3

def handle(config):
    for package in config:
        watch_process(["pip", "install", "--upgrade", "--user", package])
