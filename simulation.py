
from Cache import Cache
import constants as c


def read_word(address):
    """
    Check for the requested address in the cache for the word
    If not, go to memory, store the block containing the word in the cache

    Args:
        address: the address for the word to be returned
    
    Returns:
        word: the requested word
    """
    pass


def simulate(cache, address):    
    # compute the block offset, index, and tag
    block_offset = address & 63
    index = (address >> 6) & 15
    tag = (address >> 10) & 63
    # iterate over all of the sets in the cache until at the set that matches the index
    for s in cache.sets:
         if s == index:
             # iterate over all of the blocks in this set (this is just one block for direct-mapped)
             for b in s.blocks:
                 # check if the tag in the block matches the tag from the address and the valid flag is true
                 if b.tag == tag and b.valid:
                     # this is a cache hit, so return the word
                     # read the word at this address
                     word = read_word(address)
                     b.tag = tag  # TODO: WHY DO I NEED TO DO THIS IF THESE ARE ALREADY THE SAME?
                     b.valid = True  # TODO: " "
                     # update the rotation of the tag queue using LRU
                     for j, t in enumerate(s.tag_queue):
                         if t == tag:
                             for k in range(j, len(s.tag_queue)-1):
                                s.tag_queue[k] = s.tag.queue[k+1]     
                            s.tag_queue[-1] = tag
                            
    # else: CACHE MISS


def main():
    cache = Cache(c.NUM_SETS, c.ASSOCIATIVITY, c.CACHE_BLOCK_SIZE)
    simulate(cache, c.ADDRESS)
