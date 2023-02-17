
from Cache import Cache
import constants as c


# # compute the block offset, index, and tag
#     block_offset = address & 63
#     index = (address >> 6) & 15
#     tag = (address >> 10) & 63
#     # iterate over all of the sets in the cache until at the set that matches the index
#     for s in cache.sets:
#         if s == index:
#             # iterate over all of the blocks in this set (this is just one block for direct-mapped)
#             for b in s.blocks:
#                 # check if the tag in the block matches the tag from the address and the valid flag is true
#                 if b.tag == tag and b.valid:
#                     # CACHE HIT
#                     # read the word at this address and return it
#                     block_address = address / c.CACHE_BLOCK_SIZE
                    
#                     b.tag = tag
#                     b.valid = True
#                     # update the rotation of the tag queue using LRU
#                     for j, t in enumerate(s.tag_queue):
#                         if t == tag:
#                             for k in range(j, len(s.tag_queue)-1):
#                                 s.tag_queue[k] = s.tag.queue[k+1]     
#                             s.tag_queue[-1] = tag
#                     return word
#                 else:
#                     # CACHE MISS
#                     pass

def read_word(address):
    """
    Check for the requested address in the cache for the word
    If not, go to memory, store the block containing the word in the cache

    Args:
        cache: the cache
        address: the address for the word to be returned
    
    Returns:
        word: the requested word
    """
    pass


# initialize memory and cache
memory = [0 for i in range(c.MEMORY_SIZE)]
cache = Cache(c.NUM_SETS, c.ASSOCIATIVITY, c.CACHE_BLOCK_SIZE)

# simulate the cache with read operations
read_word(46916)
read_word(46932)
read_word(12936)
read_word(13964)
read_word(46956)
read_word(56132)
