
from Cache import Cache
import constants as c


def read_word(address):
    """
    Check for the requested address in the cache for the word
    If not, go to memory, store the block containing the word in the cache

    Args:
        address: the address for the word to be printed
    
    Returns:
        None
    """
    
    # ensure address is 4-bit aligned or in memory range, exit program as address is invalid
    assert address % 4 == 0
    assert 0 <= address < c.MEMORY_SIZE
    
    # flags for control flow during cache and memory accesses
    hit = False
    stored = False
    block_idx = -1
    
    # compute variables from address for cache/memory access
    offset = address & (c.CACHE_BLOCK_SIZE-1)
    index = (address >> c.logb2(c.CACHE_BLOCK_SIZE)) & (c.NUM_SETS-1)
    tag = address >> (c.logb2(c.CACHE_BLOCK_SIZE) + c.logb2(c.NUM_SETS))
    start_address = (address // c.CACHE_BLOCK_SIZE) * c.CACHE_BLOCK_SIZE
    
    # go to the set in the cache using the index from the address
    cache_set = cache.sets[index]
    
    # loop through the blocks in the set
    for bidx, block in enumerate(cache_set.blocks):
        # check if the data is in the cache block by comparing tags
        # if the tag is in the set, then we have a cache hit
        if block.tag == tag:
            # save block index
            block_idx = bidx
            # grab the word from the block
            word = block.data[offset] + (block.data[offset + 1] << 8) + (block.data[offset + 2] << 16) + (block.data[offset + 3] << 24)
            # update the tag queue to make sure this block's tag is moved to the front
            cache_set.tag_queue.remove(tag)
            cache_set.tag_queue.append(tag)
            # indicate we found the block in the cache
            hit = True
    
    # if the tag is not in the set, then we have to go to memory for cache miss
    if not hit:
        # grab the word and block (range of data) from memory
        word = memory[address] + c.MAX_BYTE*memory[address+1] + c.MAX_BYTE*c.MAX_BYTE*memory[address+2] + c.MAX_BYTE*c.MAX_BYTE*c.MAX_BYTE*memory[address+3]
        # loop through the blocks in the set
        for bidx, block in enumerate(cache_set.blocks):
            # determine whether every block is filled (check valid attribute)
            if not block.valid and not stored:
                # save block index
                block_idx = bidx
                # if open block exists, store the data from memory in the block and update the attributes
                block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
                block.tag = tag
                cache_set.tag_queue.remove(-1)
                cache_set.tag_queue.append(tag)
                block.valid = True
                stored = True
        # if no open block exists, we must evict one
        if not stored:
            # determine the LRU block to evit by using the tag queue
            evicted = cache_set.tag_queue.pop(0)
            # find the block in the set
            for bidx, block in enumerate(cache_set.blocks):
                if block.tag == evicted:
                    # save block index
                    block_idx = bidx
                    # replace the block with the new data and update the tag queue, set valid, and other attributes
                    block.data = block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
                    block.tag = tag
                    cache_set.tag_queue.append(tag)
                    block.valid = True
                    stored = True
            # print info about block eviction
            print(f"evict tag {evicted} in block index {block_idx}")
            print(f"read in ({start_address}-{start_address+c.CACHE_BLOCK_SIZE-1})")
        
    # print the output of the access
    print(f"read {'hit' if hit else 'miss + replace'} :: [ addr={address} index={index} block_index={block_idx} tag={tag} block_range=({start_address}-{start_address+c.CACHE_BLOCK_SIZE-1}) ]")
    print(f"  tag_queue: {cache_set.tag_queue}")
    print(f"  ADDRESS={address} {c.logb2(address)}; WORD={word}\n")

    return

def write_word(address, word):
    """
    Writes the specified word to the specified address, and will update the just the
    cache or cache and memory depending on whether it's a write-back or write-through

    Args:
        address: the location at which the word will be written
        word: the word to write
    
    Returns:
        None
    """
    
    pass


##########################
# ***run the program *** #
##########################

# initialize memory and cache
memory = bytearray(c.MEMORY_SIZE)
cache = Cache(c.NUM_SETS, c.ASSOCIATIVITY, c.CACHE_BLOCK_SIZE)

# initialize memory so that each four-byte aligned value is its index
for i in range(0, c.MEMORY_SIZE, 4):
    memory[i] = i & (c.MAX_BYTE-1)
    memory[i+1] = (i >> 8) & (c.MAX_BYTE-1)
    memory[i+2] = (i >> 16) & (c.MAX_BYTE-1)
    memory[i+3] = (i >> 24) & (c.MAX_BYTE-1)

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
