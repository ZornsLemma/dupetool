from __future__ import print_function
import hashlib
import os

# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def hash_file(filename):
    h = hashlib.md5()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


# TODO: At some point this might be extended to include a modification time (I am
# ignoring the existence of hard links) which could be used in conjunction with the
# file size to allow "safe-ish" rapid updates to an existing database of hashes; if
# the modification time and size of a file haven't changed, we can probably assume
# the hash hasn't either.
class FileInfo:
    def __init__(self, hash, size):
        self.hash = hash
        self.size = size




top = "/home/steven/archive/personal/photos/me-9"

files = {}
for dirpath, dirnames, filenames in os.walk(top):
    for filename in filenames:
        full_filename = os.path.join(dirpath, filename)
        files[full_filename] = FileInfo(hash_file(full_filename), os.path.getsize(full_filename))
for k, d in files.items():
    print(k, d.hash, d.size)
