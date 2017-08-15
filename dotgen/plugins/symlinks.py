import os

rank = 1


def handle(config):
    for symlink in config:
        Symlink(src=symlink[0], dst=symlink[1]).run()


class Symlink:
    def __init__(self, src, dst):
        pass

    def create(self):
        os.link(src, dst)

    def run(self):
        if os.path.exists(dst):
            return

        self.create()
