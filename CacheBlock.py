
class CacheBlock:
    """
    Data structure to represent a cache block for the simulation
    """
    
    def __init__(self, cache_block_size):
        self.tag = -1
        self.dirty = False
        self.valid = False
        self.data = bytearray(cache_block_size)
