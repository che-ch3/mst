from .datastore import Datastore
from .chunker import Chunker

datastore = Datastore()
chunker = Chunker(32)

class Item:
    def __init__(self, key:bytes, identifier:bytes):
        self.key:bytes = key
        self.id:bytes = identifier

class Node:
    """A node is the main data type for MSTs.
    It contains the level, starting by zero for leafs, and increasing with each
    layer of nodes.
    And it contains a ordered list of items. The items contain key and ID and
    are sorted by ther key.
    The identifier references nodes on the next lower level. The items of the
    leafs directly point to the stored values."""
    def __init__(self):
        self.level:int = 0
        self.items:tuple = ()

    def __get_leaf(self, key):
        """Returns the leaf containing the key"""
        if self.level == 0 and self.items != () and key in [item.key for item in self.items]:
            return self
        elif self.level == 0:
            # Key not found
            # FIXME return error
            return False
        # We're not at the leaf-level - pick the correct node to descend further
        # in the tree.
        for i, item in self.items:
            if i == len(self.items) and item.key <= key:
                # at last item and its key is smaller than searched key
                node = datastore.get(item.id)
                return node.get(key)
            elif item.key <= key and self.items[i+1].key > key:
                # next key is greater, so current item is the one we're looking for
                node = datastore.get(item.id)
                return node.get(key)
            else:
                # No matching item found, key must be smaller than all items
                # FIXME: rewrite for clarity
                return False

    def get(self, key):
        """Get the value for a key"""
        leaf = self.__get_leaf(key)
        if leaf == False:
            return
        for item in leaf.items:
            if item.key == key:
                return datastore.get(item.id)
        return False

    def put(self, key, value):
        """Insert a key-value pair"""
        # FIXME: readability
        if self.level == 0:
            if self.items == ():
                self.items = (Item(key, datastore.put(value)),)
            else:
                identifier = datastore.put(value)
                marksBoundary = chunker.isBoundary(identifier)
                for i, item in enumerate(self.items):
                    if key < item.key:
                        # insert key before this item
                        self.items = self.items[:i] + (Item(key, identifier),) + self.items[i:]
                        # TODO handle splitting node!
                        break
                    elif i == len(self.items) - 1:
                        # we're at the last element and the key is still larger than the item:
                        # insert as last element
                        self.items = self.items + (Item(key, identifier),)
                        # TODO handle splitting node!
                        break
                    else:
                        # We're still looking for the next bigger key
                        continue
        else:
            # TODO: Non-leaf level
            pass