from .datastore import Datastore
from .chunker import Chunker

datastore = Datastore()

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
    def __init__(self, level:int=0, pairs:tuple=(), items:tuple=(), nodes:tuple=(), chunker:Chunker=Chunker(32)):
        # FIXME redesign - inserting items and nodes should not be exposed to caller
        if pairs != () and items != () and nodes != ():
            # TODO throw error!
            # FIXME only one of the above should contain something!
            pass
        self.level:int = level
        self.items = ()
        self.chunker = chunker
        if pairs != ():
            # TODO implement and use bulk insert
            for key, value in pairs:
                self.put(key, value)
        elif nodes != ():
            self.items = tuple([Item(key, datastore.put_node(node)) for key, node in nodes])
            self.level = nodes[0][1].level + 1
        elif items != ():
            self.items = items
        recalculated = self.__recalculate()
        self.level = recalculated[1].level
        self.items = recalculated[1].items

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
        for i, item in enumerate(self.items):
            if i+1 == len(self.items) and item.key <= key:
                # at last item and its key is smaller than searched key
                node = datastore.get_node(item.id)
                return node.__get_leaf(key)
            elif item.key <= key and self.items[i+1].key > key:
                # next key is greater, so current item is the one we're looking for
                node = datastore.get_node(item.id)
                return node.__get_leaf(key)
            else:
                # No matching item found, key must be smaller than all items
                # FIXME: rewrite for clarity
                return False

    def __recalculate(self, at:int=-1):
        """Re-Calculate node.
        This was probably invoked because a split was detected and needs to be performed.
        Hence the tree upwards needs to be re-calculated as well."""
        if at != -1:
            # We got an index of a new boundary that splits a node
            # FIXME: handle the case the index indicates merging
            self.items = self.items[:at]
            node_new = Node(items=self.items[at:], chunker=self.chunker)
            return Node(level=self.level+1,
                        pairs=((self.items[0].key, self),
                               (node_new.items[0].key, node_new)
                               ),
                        chunker=self.chunker
                        )
        else:
            # TODO are we able to look for merges?
            # TODO An index was not provided - we have to look for boundaries
            nodes = [] # This contains the new (key,node)-pairs emerging from the split
            i_start = 0 # remember the starting index of the current chunk
            for i, item in enumerate(self.items[:-1]):
                if self.chunker.isBoundary(item.id):
                    # split node here
                    nodes.append((item.key, Node(level=self.level, items=self.items[i_start:i+1], chunker=self.chunker)))
                    i_start = i + 1
            if len(nodes) > 0:
                # collect leftover items in last chunk!
                nodes.append((self.items[i_start].key, Node(level=self.level, items=self.items[i_start:], chunker=self.chunker)))
            if len(nodes) > 1:
                return (nodes[0][0], Node(level=self.level+1, nodes=tuple(nodes), chunker=self.chunker))
            elif len(nodes) == 1:
                return nodes[0]
            else:
                # empty node
                return (-1, self)

    def to_tuple(self):
        if self.level == 0:
            return tuple([(item.key, datastore.get(item.id)) for item in self.items])
        else:
            ret = ()
            for item in self.items:
                ret = ret + datastore.get_node(item.id).to_tuple()
            return ret

    def get(self, key):
        """Get the value for a key"""
        leaf = self.__get_leaf(key)
        if leaf == False:
            return
        for item in leaf.items:
            if item.key == key:
                return datastore.get(item.id)
        return False

    def __put_at_leaf(self, key, value):
        """Insert a key-value pair into the leaf"""
        # Handle the leaf-level
        assert(self.level == 0)
        identifier = datastore.put(value)

        for i, item in enumerate(self.items):
            if key < item.key:
                # this loop inserts the new key before the first larger item it encounters
                self.items = self.items[:i] + (Item(key, identifier),) + self.items[i:]
                # TODO call re-computation (splitting, ...)
                if self.chunker.isBoundary(identifier):
                    self.__recalculate(at=i)
                # TODO check if key already exists
                return
        # The loop finished without identifying the proper position.
        # That means that is was greater than all items.
        # Add it to the end.
        self.items = self.items + (Item(key, datastore.put(value)),)

    def put(self, key, value):
        """Insert a key-value pair"""
        if self.level == 0:
            self.__put_at_leaf(key, value)
        else:
            # TODO: Non-leaf level
            pass

    def remove(self, key):
        """Remove the key-value pair for the specified key"""
        leaf = self.__get_leaf(key)
        if self.level == 0:
            # Handle the leaf-level
            for i, item in enumerate(self.items):
                # this loop finds the corresponding item
                if key == item.key:
                    self.items = self.items[:i] + self.items[(i+1):]
                    # TODO remove from datastore?
                    # TODO call re-computation (merging, ...)
                    return
            # The loop finished without identifying the proper position.
            # TODO: throw error
        else:
            # TODO: Non-leaf level
            pass
