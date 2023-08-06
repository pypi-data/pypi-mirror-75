import os
import tempfile
import shutil
from .randomutils import uuid4

def mkdir(folder):
    os.makedirs(folder, exist_ok=True)


def rm(filename):
    if os.path.isfile(filename):
        os.unlink(filename)
    else:
        shutil.rmtree(filename, ignore_errors=True, onerror=None)


def copy(src, dst):
    if os.path.isfile(src):
        shutil.copy2(src, dst)
    else:
        src_name = os.path.basename(src)
        dst_abspath = os.path.join(dst, src_name)
        shutil.copytree(src, dst_abspath)

def readfile(filename, binary=False, encoding="utf-8"):
    if binary:
        with open(filename, "rb") as fobj:
            return fobj.read()
    else:
        with open(filename, "r", encoding=encoding) as fobj:
            return fobj.read()

def pathjoin(path1, path2):
    return os.path.join(path1, path2)

def write(filename, data, encoding="utf-8"):
    if isinstance(data, bytes):
        with open(filename, "wb") as fobj:
            fobj.write(data)
    else:
        with open(filename, "w", encoding="utf-8") as fobj:
            fobj.write(data)


def get_temp_workspace(prefix="", makedir=True):
    folder_name = prefix + str(uuid4())
    path = os.path.abspath(os.path.join(tempfile.gettempdir(), folder_name))
    if makedir:
        mkdir(path)
    return path

def rename(filepath, name):
    folder = os.path.dirname(filepath)
    dst = os.path.abspath(os.path.join(folder, name))
    os.rename(filepath, dst)
    return dst
