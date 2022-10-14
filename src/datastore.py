from hashlib import sha512

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
