# -*- coding: utf-8 -*-
# import hashlib
import codecs
import subprocess


def hash(bytes):
    process = subprocess.Popen(
        ["sha256sum"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = process.communicate(bytes)
    return stdout.decode().strip().split()[0]


def hash_string(string):
    return hash(string.encode("utf-8"))


def hash_file(path):
    with codecs.open(path, "rb") as fhandle:
        return hash(fhandle.read())
