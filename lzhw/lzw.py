from math import floor
from .util import *

## Lempel-Ziv-Welch algorithm to compress the symbol sequences in the huffman coding dictionary
def lzw_compress(symbs):
    symbs = symbs.encode()
    keys = ascii_to_int.copy()
    n_keys = 256
    compressed = []
    start = 0
    n_symbs = len(symbs) + 1
    while True:
        if n_keys >= 512:
            keys = ascii_to_int.copy()
            n_keys = 256
        for i in range(1, n_symbs - start):
            w = symbs[start:start + i]
            if w not in keys:
                compressed.append(keys[w[:-1]])
                keys[w] = n_keys
                start += i - 1
                n_keys += 1
                break
        else:
            compressed.append(keys[w])
            break
    bits = bit_fill(compressed)
    return byte_encode(bits, to_bytes = False)

def lzw_decompress(encoded):
    if isinstance(encoded, int):
        encoded = encoded.to_bytes(ceil(encoded.bit_length() / 8), "big")
    keys = int_to_ascii.copy()
    bits = byte_decode(encoded)
    n_extended_bytes = floor(len(bits) / 9)
    bits = bits[-n_extended_bytes * 9:]
    data_list = byte2int(bits, n_extended_bytes)
    previous = keys[data_list[0]]
    uncompressed = [previous]
    n_keys = 256
    for i in data_list[1:]:
        if n_keys >= 512:
            keys = int_to_ascii.copy()
            n_keys = 256

        current = keys.get(i)
        if not current:
            current = previous + previous[:1]

        uncompressed.append(current)
        keys[n_keys] = previous + current[:1]
        previous = current
        n_keys += 1

    return b"".join(uncompressed).decode()
