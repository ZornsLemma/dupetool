# TODO: At some point this might be extended to include a modification time (I am
# ignoring the existence of hard links) which could be used in conjunction with the
# file size to allow "safe-ish" rapid updates to an existing database of hashes; if
# the modification time and size of a file haven't changed, we can probably assume
# the hash hasn't either. If I were to also do a byte-for-byte comparison before
# deleting that would also help make such things safer.
class FileInfo:
    def __init__(self, hash, size):
        self.hash = hash
        self.size = size
