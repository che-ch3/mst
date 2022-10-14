from hashlib import sha512
from pickle import dumps, loads

class Datastore:
    def __init__(self):
        self.store = {}

    def get(self, identifier:bytes):
        if identifier in self.store.keys():
            return self.store[identifier]
        else:
            return False

    def put(self, value):
        identifier = sha512(value).digest()
        self.store[identifier] = value
        return identifier

    def get_node(self, identifier:bytes):
        if identifier in self.store.keys():
            return loads(self.store[identifier])
        else:
            return False

    def put_node(self, value):
        value_b = dumps(value)
        identifier = sha512(value_b).digest()
        self.store[identifier] = value_b
        return identifier
