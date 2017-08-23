# -*- coding: utf-8 -*-
from dotgen.process import watch_process

import os

rank = 0


def handle(config):
    for gitmodule in config:
        GitModule(
            path=config[gitmodule]["path"],
            url=config[gitmodule]["url"],
            depth=config[gitmodule].get("depth", None)).run()


class GitModule:
    def __init__(self, path, url, **kwargs):
        self.path = path
        self.url = url
        self.depth = kwargs["depth"]

    def clone(self):
        cmd = ["git", "clone", self.url, self.path]
        if self.depth:
            cmd += ["--depth", str(self.depth)]
        watch_process(cmd)

    def run(self):
        if os.path.exists(os.path.join(self.path, ".git")):
            pass

        self.clone()
