'''
Used for Python 3.5
from contextlib import redirect_stderr

with open('filename.log', 'w') as stderr, redirect_stderr(stderr):
    print(test["name"])
'''
import sys, traceback

try:
    print(list[file]) # Used to create a NameError
except:
    traceback.print_exc(file=open("lg.txt", "w"))
