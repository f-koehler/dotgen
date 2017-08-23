# -*- coding: utf-8 -*-
# from dotgen.process import watch_process
import subprocess
import sys

import os

rank = 0


def handle(output_dir, config):
    for gitmodule in config:
        GitModule(
            path=os.path.join(output_dir, config[gitmodule]["path"]),
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
        subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)
        # watch_process(cmd)

    def run(self):
        if os.path.exists(os.path.join(self.path, ".git")):
            pass

        self.clone()
