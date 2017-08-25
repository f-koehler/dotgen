# -*- coding: utf-8 -*-
from colorama import Fore
import os

rank = 1


def handle(output_dir, config):
    for symlink in config:
        print(Fore.WHITE + "symlink: {} -> {}".format(symlink[0], symlink[1]) +
              Fore.RESET)
        Symlink(
            src=os.path.join(output_dir, symlink[0]),
            dst=os.path.join(output_dir, symlink[1])).run()
        print(Fore.WHITE + "done\n" + Fore.RESET)


class Symlink:
    def __init__(self, src, dst):
        self.src = os.path.abspath(src)
        self.dst = os.path.abspath(dst)

    def run(self):
        if os.path.exists(self.dst):
            return

        dir = os.path.dirname(self.dst)
        if not os.path.exists(dir):
            os.makedirs(dir)

        os.symlink(self.src, self.dst)
