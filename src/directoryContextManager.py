# !/usr/bin/python3

from os import getcwd, chdir
from contextlib import contextmanager

@contextmanager
def workInDirectory(newDir):

    currDir = getcwd()
    
    try:
        chdir(newDir)
        yield
    finally:
        chdir(currDir)