class Chunker:
    """The chunking factor determines the expected average node size. (A chunking factor of 2 should result in approximately binary trees."""
    def __init__(self, chunkingFactor:int):
        if chunkingFactor < 2 or chunkingFactor > 65:
            # Throw error!
            pass
        self.chunkingFactor:int = chunkingFactor
        # This is essentially no correct implementation, but should approximately work:
        self.comparer = (((2**8)**(65-chunkingFactor))-1).to_bytes(64,'big',signed=True)

    def isBoundary(self, identifier:bytes):
        if self.comparer > identifier:
            # The respective identifier marks a boundary within its node
            return True
        else:
            # The respective identifier does NOT mark a boundary
            return False

