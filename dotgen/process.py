from __future__ import print_function

import subprocess
import threading


def watch_process(cmd, stdout_handler=None, stderr_handler=None, **kwargs):
    def default_handler(line):
        print(line)

    if not stdout_handler:
        stdout_handler = default_handler
    if not stderr_handler:
        stderr_handler = default_handler

    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.PIPE
    proc = subprocess.Popen(cmd, **kwargs)

    def pipe_watcher(pipe, handler):
        with pipe:
            for line in iter(pipe.readline, ""):
                handler(line.strip("\n"))

    threading.Thread(target=pipe_watcher, args=[proc.stdout, stdout_handler]).start()
    threading.Thread(target=pipe_watcher, args=[proc.stderr, stderr_handler]).start()

    return_code = proc.wait()
    if return_code:
        raise subprocess.CalledProcessError("\n".join(cmd), return_code)
