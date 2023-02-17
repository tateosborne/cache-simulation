import CacheSet
import constants as c


class Cache:
    """
    Data structure to represent a cache for the simulation
    """
    def __init__(self, num_sets, associativity, cache_block_size):
        self.write_through = False
        self.sets = [CacheSet(cache_block_size, associativity) for i in range(num_sets)]
        memory_size_bits = logb2(c.MEMORY_SIZE)
        self.cache_size_bits = logb2(c.CACHE_SIZE)
        self.cache_block_size_bits = logb2(c.CACHE_BLOCK_SIZE)
        self.index_length = logb2(c.NUM_SETS)
        self.block_offset_length = logb2(c.CACHE_BLOCK_SIZE)

def logb2(val):
    i = 0
    assert val>0
    while val>0:
        i=i+1
        val=val>>1
    return i-1