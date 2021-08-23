from __future__ import print_function
import os
import pickle
import sys
from fileinfo import FileInfo


def die(s):
    print(s, file=sys.stderr)
    sys.exit(1)


with open("foo.pickle", "rb") as f:
    files = pickle.load(f)

remove_duplicates_under = "/home/steven/archive/personal/photos/from-keyone-to-sort-2021-08-22"

found = False
for filename in files:
    if filename.startswith(remove_duplicates_under):
        found = True
        break
if not found:
    die("There are no files under '%s'!" % remove_duplicates_under)
