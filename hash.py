from __future__ import print_function
import hashlib
import os
import pickle
from fileinfo import FileInfo

# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def hash_file(filename):
    h = hashlib.md5()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()




top = "/home/steven/archive/personal/photos"

# TODO: How will I deal with paths? To some extent always working with full paths
# is good, but I may end up shuffling files around during a cleanup process and
# ideally it would be possible to avoid regenerating the hashes.

files = {}
for dirpath, dirnames, filenames in os.walk(top):
    for filename in filenames:
        full_filename = os.path.join(dirpath, filename)
        files[full_filename] = FileInfo(hash_file(full_filename), os.path.getsize(full_filename))
for k, d in files.items():
    print(k, d.hash, d.size)

with open("foo.pickle", "wb") as f:
    pickle.dump(files, f, protocol=pickle.HIGHEST_PROTOCOL)
