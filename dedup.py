from __future__ import print_function
import collections
import os
import pickle
import sys
from fileinfo import FileInfo


def die(s):
    print(s, file=sys.stderr)
    sys.exit(1)


def confirm_identical(a, b):
    return True # SFTODO! CHECK CONTENTS, PROBABLY ALSO COMPARE INODES


with open("foo.pickle", "rb") as f:
    files = pickle.load(f)

hashes = collections.defaultdict(set)
for filename, fi in files.items():
    hashes[fi.hash].add(filename)

remove_duplicates_under = "/home/steven/archive/personal/photos/from-keyone-to-sort-2021-08-22"

candidate_filenames = []
for filename in files:
    if filename.startswith(remove_duplicates_under):
        candidate_filenames.append(filename)

# Sanity check to detect typos or differences in path initial prefixes.
if len(candidate_filenames) == 0:
    die("There are no files under '%s'!" % remove_duplicates_under)

for candidate_filename in candidate_filenames:
    candidate_hash = files[candidate_filename].hash
    other_filenames = hashes[candidate_hash] - set([candidate_filename])
    if len(other_filenames) > 0:
        for other_filename in other_filenames:
            if confirm_identical(candidate_filename, other_filename):
                print("Could remove '%s'; '%s' is identical" % (candidate_filename, other_filename))
                break
            else:
                print("warning: '%s' and '%s' share a hash but are not identical" % (candidate_filename, other_filename))
