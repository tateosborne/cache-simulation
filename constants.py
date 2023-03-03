
# helper function for calculating log_2
def logb2(val):
    i = 0
    assert val > 0
    while val > 0:
        i += 1
        val = val >> 1
    return i - 1

# cache properties
MEMORY_SIZE = 65536  # 2^16
CACHE_SIZE = 1024  # 2^10
CACHE_BLOCK_SIZE = 64  # 2^6
ASSOCIATIVITY = 2

ADDRESS_LENGTH = 65536

# calculated features
NUM_BLOCKS = CACHE_SIZE // CACHE_BLOCK_SIZE
NUM_SETS = NUM_BLOCKS // ASSOCIATIVITY
TAG_LENGTH = logb2(ADDRESS_LENGTH) - logb2(CACHE_BLOCK_SIZE) - logb2(NUM_SETS)

# to ensure four-byte alignment
MAX_BYTE = 256
