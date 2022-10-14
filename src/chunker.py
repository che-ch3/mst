class Chunker:
    """This is a minimail Implementation of a chunker.
    It determines the boundaries between chunks by comparing the ID (hash) of an element with a certain value - the chunking factor.
    This chunking factor determines the probability with which a certain item is a boundary and thus determines the average node size.
    (A chunking factor of 2 should result in approximately binary trees.)"""

    def __init__(self, chunkingFactor:int):
        if chunkingFactor < 2 or chunkingFactor > 65:
            # Throw error!
            pass
        self.chunkingFactor:int = chunkingFactor
        # This converts the factor in a format that is more usable later on.
        # The basic idea is to create a byte array of the size of the ID (hash).
        # This byte array can be easily compared to IDs (hashes).
        # The chunking factor determines the corresponding number of leading zeros.
        # Thus by comparing it to the identifier we get a result with a probability that depends on the chunking factor.
        # A chunking factor of two results in all but the first bit being one.
        # Every second uniformly generated ID (hash) is smaller.
        # A chunking factor of three results in the first two bits being one.
        # Only every fourth ID (hash) is smaller.
        # FIXME: This is essentially no correct implementation, but should approximately work:
        self.comparer = (((2**8)**(65-chunkingFactor))-1).to_bytes(64,'big',signed=True)

    def isBoundary(self, identifier:bytes):
        if self.comparer > identifier:
            # The respective identifier marks a boundary within its node
            return True
        else:
            # The respective identifier does NOT mark a boundary
            return False

