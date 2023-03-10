
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
    
    # flags for control flow during cache and memory accesses and initialize block index
    hit = False
    stored = False
    eviction = False
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
        # check if the data is in the cache block by comparing tags: if the tag is in the set, then we have a cache hit
        if block.tag == tag and block.valid:
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
        # grab the word from memory
        word = memory[address] + c.MAX_BYTE*memory[address+1] + c.MAX_BYTE*c.MAX_BYTE*memory[address+2] + c.MAX_BYTE*c.MAX_BYTE*c.MAX_BYTE*memory[address+3]
        # loop through the blocks in the set
        for bidx, block in enumerate(cache_set.blocks):
            # if there's an open block in the set, use that
            if not block.valid and not stored:
                # save block index
                block_idx = bidx
                # store the data from memory in the block and update the block's attributes
                block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
                block.tag = tag
                block.valid = True
                # add the tag to the tag queue
                cache_set.tag_queue.remove(-1)
                cache_set.tag_queue.append(tag)
                # indicate we have stored the memory block so we don't store it in another block
                stored = True
        # if no open block in the set exists, we must evict one
        if not stored:
            # determine the LRU block to evict by using the tag queue (tag at the back)
            evicted_tag = cache_set.tag_queue.pop(0)
            for bidx, block in enumerate(cache_set.blocks):
                # find the block we will evict
                if block.tag == evicted_tag:
                    # save block index
                    block_idx = bidx
                    # copy the evicted block in case we need to write to memory
                    evicted_block = cache_set.blocks[block_idx]
                    # replace the block with the new data and update the block's attributes
                    block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
                    block.tag = tag
                    block.valid = True
                    # add this new block's tag to the front of the tag queue
                    cache_set.tag_queue.append(tag)
                    # indicate that we evicted a block
                    eviction = True
                    # check if write-back or write-through cache: if write-back and dirty bit of evicted block is flagged, we need to update memory
                    if not cache.write_through and evicted_block.dirty:
                        # form the address in memory where this block's data is stored
                        evicted_start_addr = (evicted_tag << c.logb2(c.NUM_SETS)) + index
                        evicted_start_addr <<= c.logb2(c.CACHE_BLOCK_SIZE)
                        # update memory with the evicted block since it holds updated data that's not currently in memory
                        for i in range(0, c.CACHE_BLOCK_SIZE, 4):
                            memory[evicted_start_addr+i] = evicted_block.data[i]
                    
    # print the output describing this access to cache/memory
    print(f"\nread {'hit' if hit else 'miss + replace'} [addr={address} index={index} block_index={block_idx} tag={tag}]: word={word} ({start_address}-{start_address+c.CACHE_BLOCK_SIZE-1})")
    if eviction:
        print(f"evict tag {evicted_tag} in block index {block_idx}")
    if not hit:
        print(f"read in ({start_address}-{start_address+c.CACHE_BLOCK_SIZE-1})")
    if not cache.write_through and eviction and evicted_block.dirty:
        print(f"write back ({evicted_start_addr}-{evicted_start_addr+c.CACHE_BLOCK_SIZE-1})")
    print(f"tag_queue for set {index}: {cache_set.tag_queue}")
    print(f"address={address}; word={word}")

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
    
    # ensure address is 4-bit aligned or in memory range, exit program as address is invalid
    assert address % 4 == 0
    assert 0 <= address < c.MEMORY_SIZE
    
    # flags for control flow during cache and memory accesses and initialize block index
    hit = False
    stored = False
    eviction = False
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
        # check if the block containing the address is in the cache block by comparing tags: if the tag is in the set, then we have a cache hit
        if block.tag == tag and block.valid:
            # save block index
            block_idx = bidx
            # write the word to the block in the cache
            block.data[offset] = word
            block.data[offset+1] = word >> 8
            block.data[offset+2] = word >> 16
            block.data[offset+3] = word >> 24
            # update the tag queue to make sure this block's tag is moved to the front
            cache_set.tag_queue.remove(tag)
            cache_set.tag_queue.append(tag)
            # check if write-back or write-through cache: if we're using a write-back cache, mark dirty bit so we know to write the block to memory upon eviction
            if not cache.write_through:
                block.dirty = True
            # if we're using a write-through cache, we just write the word to memory now
            else:
                # update the memory with the new word
                memory[address] = word
                memory[address+1] = word // (c.MAX_BYTE)
                memory[address+2] = word // (c.MAX_BYTE*c.MAX_BYTE)
                memory[address+3] = word // (c.MAX_BYTE*c.MAX_BYTE*c.MAX_BYTE)
            # indicate we found the block in the cache
            hit = True

    # if the tag is not in the set, then we have to go to memory for cache miss
    if not hit:
        # write the word to memory
        memory[address] = word
        memory[address+1] = word // (c.MAX_BYTE)
        memory[address+2] = word // (c.MAX_BYTE*c.MAX_BYTE)
        memory[address+3] = word // (c.MAX_BYTE*c.MAX_BYTE*c.MAX_BYTE)
        # loop through the blocks in the set
        for bidx, block in enumerate(cache_set.blocks):
            # if there's an open block in the set, use that
            if not block.valid and not stored:
                # save block index
                block_idx = bidx
                # store the data from memory in the block and update the block's attributes
                block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
                block.tag = tag
                block.valid = True
                # add the block's tag to the front of the set's tag queue
                cache_set.tag_queue.remove(-1)
                cache_set.tag_queue.append(tag)
                # indicate we have stored the data in the cache
                stored = True
        # if no open block exists, we must evict one
        if not stored:
            # determine the LRU block to evict by using the tag queue (tag at the back)
            evicted_tag = cache_set.tag_queue.pop(0)
            for bidx, block in enumerate(cache_set.blocks):
                # find the block we will evict
                if block.tag == evicted_tag:
                    # save block index
                    block_idx = bidx
                    # copy the evicted block in case we need to write to memory
                    evicted_block = cache_set.blocks[block_idx]
                    # replace the block with the new data and update the block's attributes
                    block.data = memory[start_address : start_address+c.CACHE_BLOCK_SIZE]
                    block.tag = tag
                    block.valid = True
                    # add this new block's tag to the front of the tag queue
                    cache_set.tag_queue.append(tag)
                    # indicate that we evicted a block
                    eviction = True
                    # check if write-back or write-through cache: if write-back and dirty bit of evicted block is flagged, we need to update memory
                    if not cache.write_through and evicted_block.dirty:
                        # form the address in memory where this block's data is stored
                        evicted_start_addr = (evicted_tag << c.logb2(c.NUM_SETS)) + index
                        evicted_start_addr <<= c.logb2(c.CACHE_BLOCK_SIZE)
                        # update memory with the evicted block since it holds updated data that's not currently in memory
                        for i in range(c.CACHE_BLOCK_SIZE):
                            memory[evicted_start_addr+i] = evicted_block.data[i]
                                
    # print the output describing this access to cache/memory
    print(f"\nwrite {'hit' if hit else 'miss + replace'} [addr={address} index={index} block_index={block_idx} tag={tag}]: word={word} ({start_address}-{start_address+c.CACHE_BLOCK_SIZE-1})")
    if eviction:
        print(f"evict tag {evicted_tag} in block index {block_idx}")
    if not hit:
        print(f"read in ({start_address}-{start_address+c.CACHE_BLOCK_SIZE-1})")
    if not cache.write_through and eviction and evicted_block.dirty:
        print(f"write back ({evicted_start_addr}-{evicted_start_addr+c.CACHE_BLOCK_SIZE-1})")
    print(f"tag_queue for set {index}: {cache_set.tag_queue}")
    if cache.write_through:
        print(f"write-through cache: write {word} to memory[{address}]")
    
    return


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
if cache.write_through:
    print(f"write through")
else:
    print(f"write back")
print("--------------------------------")

# simulate the cache with read and write operations and print output
read_word(1152)
read_word(2176)
read_word(3200)
read_word(4224)
read_word(5248)
read_word(7296)
read_word(4224)
read_word(3200)
write_word(7312, 17)
read_word(7320)
read_word(4228)
read_word(3212)
write_word(5248, 5)
read_word(5248)
write_word(8320, 7)
read_word(8324)
read_word(9344)
read_word(11392)
read_word(16512)
read_word(17536)
read_word(8320)
read_word(17536)
read_word(17532)
