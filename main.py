import hashlib
import time
from model import Model
from rpc import BroadCast

class Block(Model):
    def __init__(self,tx,timestamp, index, previous_hash):
        self.index = index
        self.tx = tx
        self.timestamp = timestamp
        self.previous_block = previous_hash

    def header_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.tx) +
                               str(self.previous_block)).encode('utf-8')).hexdigest()

    def pow(self):
        nouce = 0
        while self.valid(nouce) is False:
            nouce += 1
        self.nouce = nouce
        return nouce

    def make(self,nouce):
        self.hash = self.ghash(nouce)

    def ghash(self, nouce):
        header_hash = self.header_hash()
        token = ''.join((header_hash, str(nouce))).encode('utf-8')
        return hashlib.sha256(token).hexdigest()

    def valid(self, nouce):
        return self.ghash(nouce)[:4] == "0000"

    def to_dict(self):
        return self.__dict__

    def from_dict(cls, bdict):
        b = cls(bdict['index'], bdict['timestamp'], bdict['tx'], bdict['previous_block'])
        b.hash = bdict['hash']
        b.nouce = bdict['nouce']
        return b

    @staticmethod
    def spread(block):
        BroadCast().new_block(block)