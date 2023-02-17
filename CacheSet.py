
import CacheBlock

class CacheSet:
    """
    Data structure to represent a cache set for the simulation
    """
    
    def __init__(self, cache_block_size, associativity):
        self.blocks = [CacheBlock(cache_block_size) for i in range(associativity)]
        self.tag_queue = [-1 for i in range(associativity)]
