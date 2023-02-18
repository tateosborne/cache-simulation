
from Cache import Cache
import constants as c


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
    outcome = ""
    
    # compute variables from address for cache/memory access
    offset = address % c.NUM_SETS
    index = address // c.CACHE_BLOCK_SIZE
    tag = (address >> 10) & 63
    start_address = index * c.CACHE_BLOCK_SIZE
    
    # go to the index in the cache where the address would be if in the cache
    target_set = cache.sets[index]
    # for a direct-mapped cache, there is one block in each set
    target_block = target_set[0]
    # check if the tag in this block in the cache
    if target_block.tag == tag:
        # this is cache hit, so retrieve the data from the cache and set hit flag
        word = target_block.data[offset]
        outcome = "hit"
    else:
        # this is a cache miss, so go to memory for the value
        word = memory[address] + 256*memory[address+1] + 256*256*memory[address+2] + 256*256*256*memory[address+3]
        # load the block into the cache
        # iterate through memory starting at the start address for the block
        for i in range(64):
            byte = 8*i
            # store the block in the cache
            target_block.data[i] = memory[start_address+(byte)]
                
        # update the tag queue, which is going to have one element for direct-mapped
        target_set.tag_queue[0] = tag
        # set the valid flag so we know the cache is loaded accurately
        target_block.valid = True
        outcome = "miss"
    
    print(f"read {outcome} [ addr={address} index={index} tag={tag}: word={word} ({start_address} - {start_address + c.CACHE_BLOCK_SIZE - 1}) ]")
    print(f"{target_set.tag_queue}")
    
    return word


##########################
# ***run the program *** #
##########################

# initialize memory and cache
memory = bytearray(c.MEMORY_SIZE)
cache = Cache(c.NUM_SETS, c.ASSOCIATIVITY, c.CACHE_BLOCK_SIZE)

# print cache parameters
print("--------------------------------")
print(f"cache size: {c.CACHE_SIZE}")
print(f"block size: {c.CACHE_BLOCK_SIZE}")
print(f"num blocks: {c.NUM_BLOCKS}")
print(f"num sets: {c.NUM_SETS}")
print(f"associativity: {c.ASSOCIATIVITY}")
print(f"tag length: {c.TAG_LENGTH}")
print("--------------------------------")

# simulate the cache with read operations and print output
word = read_word(46916)
read_word(46932)
read_word(12936)
read_word(13964)
read_word(46956)
read_word(56132)
