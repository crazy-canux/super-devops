import os


def expandpath(path):
    if path:
        real_path = path
        if '~' in path:
            real_path = os.path.expanduser(path)
        if '$' in path:
            real_path = os.path.expandvars(path)
        return real_path