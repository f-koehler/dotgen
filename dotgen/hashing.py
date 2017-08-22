import hashlib
import codecs


def hash(bytes):
    m = hashlib.sha256()
    m.update(bytes)
    return m.digest()


def hash_string(string):
    return hash(string.encode("utf-8"))


def hash_file(path):
    with codecs.open(path, "r", "utf-8") as fhandle:
        return hash_string(fhandle.read())
