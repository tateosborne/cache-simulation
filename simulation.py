
from Cache import Cache, logb2
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
    
    # ensure address is 4-bit aligned or in memory range, exit program as address is invalid
    assert address % 4 == 0
    assert 0 <= address < c.MEMORY_SIZE
    
    # var to store the status of whether the access was a cache hit or miss
    outcome = ""
    
    # compute variables from address for cache/memory access
    offset = address & 63
    index = (address >> 6) & 15
    tag = (address >> 10) & 63
    start_address = (address // c.CACHE_BLOCK_SIZE) * c.CACHE_BLOCK_SIZE
    
    # go to the index in the cache where the address would be if in the cache
    target_set = cache.sets[index]
    # for a direct-mapped cache, there is one block in each set
    target_block = target_set.blocks[0]
    # check if the tag in this block in the cache
    if target_block.tag == tag:
        # this is cache hit, so retrieve the data from the cache and set hit flag
        word = target_block.data[offset] + (target_block.data[offset + 1] << 8) + (target_block.data[offset + 2] << 16) + (target_block.data[offset + 3] << 24)
        outcome = "hit"
        
    else:
        # print tag of block being evicted and the new block's tag
        if target_set.tag_queue[0] != -1:
            print(f"evict tag {target_set.tag_queue[0]} in block index 0")
            print(f"read in ({start_address} - {start_address+c.CACHE_BLOCK_SIZE-1})")
            
        # for direct mapped, tag queue consists of one tag, as block index = 0.
        # replace the tag with the new one
        target_set.tag_queue[0] = tag
        
        # set the valid flag so we know the cache is loaded accurately
        target_block.valid = True
        
        # this is a cache miss, so go to memory for the value
        word = memory[address] + c.MAX_BYTE*memory[address+1] + c.MAX_BYTE*c.MAX_BYTE*memory[address+2] + c.MAX_BYTE*c.MAX_BYTE*c.MAX_BYTE*memory[address+3]
               
        # load the block into the cache
        target_block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
        
        outcome = "miss + replace"
    
    # print output of each read
    print(f"read {outcome} [addr={address} index={index} tag={tag}: word={word} ({start_address} - {start_address+c.CACHE_BLOCK_SIZE-1})]")
    print(f"{target_set.tag_queue}")
    print(f"address = {address} {logb2(address)}; word = {word}")
    
    return


##########################
# ***run the program *** #
##########################

# initialize memory and cache
memory = bytearray(c.MEMORY_SIZE)
cache = Cache(c.NUM_SETS, c.ASSOCIATIVITY, c.CACHE_BLOCK_SIZE)

# initialize memory so that each four-byte aligned value is its index
for i in range(0, c.MAX_BYTE+1, 4):
    memory[i] = i & c.MAX_BYTE
    memory[i+1] = (i >> 8) & c.MAX_BYTE
    memory[i+2] = (i >> 16) & c.MAX_BYTE
    memory[i+3] = (i >> 24) & c.MAX_BYTE

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
read_word(46916)
read_word(46932)
read_word(12936)
read_word(13964)
read_word(46956)
read_word(56132)
