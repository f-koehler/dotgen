# -*- coding: utf-8 -*-
import os

rank = 1


def handle(output_dir, config):
    for symlink in config:
        Symlink(
            src=os.path.join(output_dir, symlink[0]),
            dst=os.path.join(output_dir, symlink[1])).run()


class Symlink:
    def __init__(self, src, dst):
        self.src = os.path.abspath(src)
        self.dst = os.path.abspath(dst)

    def run(self):
        if os.path.exists(self.dst):
            return

        os.symlink(self.src, self.dst)
