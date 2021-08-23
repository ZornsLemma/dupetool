from __future__ import print_function
import collections
import os
import pickle
import sys
from fileinfo import FileInfo


def die(s):
    print(s, file=sys.stderr)
    sys.exit(1)


# Return True iff a is a symlink to b
# https://stackoverflow.com/questions/17889368/if-path-is-symlink-to-another-path
def is_symlink(a, b):
    return os.path.islink(a) and os.path.realpath(a) == os.path.realpath(b)


def files_related(a, b):
    return is_symlink(a, b) or is_symlink(b, a)


def file_content_identical(a, b):
    BUF_SIZE = 4096
    with open(a, "rb") as af:
        with open(b, "rb") as bf:
            while True:
                ad = af.read(BUF_SIZE)
                bd = bf.read(BUF_SIZE)
                if len(ad) == 0 and len(bd) == 0:
                    return True
                if ad != bd:
                    return False


with open("foo.pickle", "rb") as f:
    files = pickle.load(f)

hashes = collections.defaultdict(set)
for filename, fi in files.items():
    hashes[fi.hash].add(filename)

remove_duplicates_under = "/home/steven/archive/personal/photos/from-keyone-to-sort-2021-08-22"

candidate_filenames = set()
for filename in files:
    if filename.startswith(remove_duplicates_under):
        candidate_filenames.add(filename)

# Sanity check to detect typos or differences in path initial prefixes.
if len(candidate_filenames) == 0:
    die("There are no files under '%s'!" % remove_duplicates_under)

for candidate_filename in candidate_filenames:
    candidate_hash = files[candidate_filename].hash
    # Note that we remove *all* candidate_filenames in the next line; this protects
    # us if the same content appears multiple times in the candidates but *not*
    # anywhere else. TODO: test this works! i.e. set up that case and confirm we don't remove either candidate (arguably we should remove at least one,  or warn about this, but I think there's an argument to be made for leaving well alone)
    other_filenames = hashes[candidate_hash] - candidate_filenames
    if len(other_filenames) > 0:
        for other_filename in other_filenames:
            if files_related(candidate_filename, other_filename):
                # TODO: Issue a warning?
                break
            elif file_content_identical(candidate_filename, other_filename):
                print("Could remove '%s'; '%s' is identical" % (candidate_filename, other_filename))
                break
            else:
                print("warning: '%s' and '%s' share a hash but are not identical" % (candidate_filename, other_filename))
