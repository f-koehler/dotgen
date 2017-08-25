# -*- coding: utf-8 -*-
from colorama import Fore
import os
import re
import subprocess
import sys

rank = 0


def handle(output_dir, config):
    for gitmodule in config:
        print(Fore.WHITE + "module: " + gitmodule + Fore.RESET)
        GitModule(
            path=os.path.join(output_dir, config[gitmodule]["path"]),
            url=config[gitmodule]["url"],
            depth=config[gitmodule].get("depth", None)).run()
        print(Fore.WHITE + "done\n" + Fore.RESET)


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

    def get_current_branch(self):
        regex = re.compile(r"^\*\s+(.+)$")

        process = subprocess.Popen(
            ["git", "branch"],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=sys.stderr)
        stdout, _ = process.communicate()
        stdout = stdout.decode().splitlines()

        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode,
                                                ["git", "branch"])

        for line in stdout:
            m = regex.match(line)
            if m:
                return m.group(1)

        raise RuntimeError("Failed to determine git branch name")

    def run(self):
        if os.path.exists(os.path.join(self.path, ".git")):
            self.update()
            return

        self.clone()

    def update(self):
        branch = self.get_current_branch()

        process = subprocess.Popen(
            ["git", "pull", "origin", branch],
            cwd=self.path,
            stdout=sys.stdout,
            stderr=sys.stderr)
        if process.wait():
            raise subprocess.CalledProcessError(
                process.returncode, ["git", "pull", "origin", branch])
