import os
Path = os.path


def brother(path, name):
    return Path.join(Path.dirname(path), name)