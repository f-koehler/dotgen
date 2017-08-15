import subprocess
import threading


def watch_process(cmd,
                  stdout_handler=lambda l: print(l),
                  stderr_handler=lambda l: print(l),
                  **kwargs):
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.PIPE
    proc = subprocess.Popen(cmd, **kwargs)

    def pipe_watcher(pipe, handler):
        for line in iter(proc.stdout.readline, ""):
            handler(line.strip("\n"))

    threading.Thread(target=pipe_watcher, args=(proc.stdout, stdout_handler))
    threading.Thread(target=pipe_watcher, args=(proc.stderr, stderr_handler))

    return_code = proc.wait()

    if return_code:
        raise subprocess.CalledProcessError("\n".join(cmd), return_code)
