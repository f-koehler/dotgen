# -*- coding: utf-8 -*-
from colorama import Fore
import math
import os
import requests
import subprocess
import tqdm

from dotgen import hashing

rank = 0


def handle(output_dir, config):
    for download in config:
        print(Fore.WHITE + "download: " + download + Fore.RESET)
        cfg = config[download]
        download_path = os.path.join(output_dir, cfg["path"])

        hash_cfg = cfg["hash"]

        if os.path.exists(download_path):
            hash = hashing.hash_file(download_path)
            if hash != hash_cfg:
                os.remove(download_path)
            continue

        dir = os.path.dirname(download_path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        req = requests.get(cfg["url"], stream=True)
        size = int(req.headers.get("content-length"))
        chunk_size = 2048
        with open(download_path, "wb") as fhandle:
            with tqdm.tqdm(total=size) as pbar:
                for chunk in req.iter_content(chunk_size=chunk_size):
                    out = fhandle.write(chunk)
                    if out < 0:
                        out = 0
                    pbar.update(out)

        hash = hashing.hash_file(download_path)
        if hash != hash_cfg:
            os.remove(download_path)
            continue

        if "chmod" in cfg:
            subprocess.call(["chmod", str(cfg["chmod"]), download_path])

        print(Fore.WHITE + "done\n" + Fore.RESET)
