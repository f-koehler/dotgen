#!/usr/bin/env python
import pkgutil

from dotgen.process import watch_process

if __name__ == "__main__":
    cmd = ["pyinstaller", "--onefile", "--name", "dotgen", "--strip"]

    import dotgen.plugins as plugins
    for info in pkgutil.iter_modules(plugins.__path__):
        print(info)
        cmd += ["--hidden-import", "dotgen.plugins." + info[1]]

    cmd.append("dotgen/__main__.py")

    watch_process(cmd)
