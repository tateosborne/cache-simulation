
ASSOCIATIVITY    = 1
MEMORY_SIZE      = 65536  # 2^16
CACHE_SIZE       = 1024  # 2^10
CACHE_BLOCK_SIZE = 64  # 2^6
NUM_BLOCKS = CACHE_SIZE // CACHE_BLOCK_SIZE
NUM_SETS = NUM_BLOCKS // ASSOCIATIVITY
TAG_LENGTH = MEMORY_SIZE // CACHE_SIZE
MAX_BYTE = 255 # ranges from 0-255
