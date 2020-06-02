from math import floor, ceil
from cpython cimport int as Integer

ctypedef fused str_or_byte:
    bytes
    str

cdef str bit_fill(list comp):
    cdef Integer i
    cdef str s = "1" + "".join([bin(i)[2:].zfill(9) for i in comp])
    return s

cdef Integer byte_encode(str bits):
    cdef Integer i = int(bits, 2)
    return i

cdef str byte_decode(str_or_byte enc):
    cdef str bins = bin(int.from_bytes(enc, "big"))[2:].zfill(len(enc) * 8)
    return bins

cdef list byte2int(str bits, int ext_bytes):
    cdef int i
    cdef list lst = [int(bits[i * 9:(i + 1) * 9], 2) for i in range(ext_bytes)]
    return lst

cdef int i, ib
cdef dict ascii_to_int = {i.to_bytes(1, "big"): i for i in range(256)}

cdef bytes b
cdef dict int_to_ascii = {ib: b for b, ib in ascii_to_int.items()}

## Lempel-Ziv-Welch algorithm to compress the symbol sequences in the huffman coding dictionary
cpdef Integer lzw_compress(str symb):
    cdef bytes symbs = symb.encode()
    cdef dict keys = ascii_to_int.copy()
    cdef int n_keys = 256
    cdef list compressed = []
    cdef int start = 0
    cdef int n_symbs = len(symbs) + 1
    cdef int i
    cdef bytes w
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
    cdef str bits = bit_fill(compressed)
    cdef Integer benc = byte_encode(bits)
    return benc

cpdef str lzw_decompress(Integer encoded):
    cdef bytes encod = encoded.to_bytes(ceil(encoded.bit_length() / 8), "big")
    cdef dict keys = int_to_ascii.copy()
    cdef str bits = byte_decode(encod)
    cdef int n_extended_bytes = floor(len(bits) / 9)
    cdef str bitss = bits[-n_extended_bytes * 9:]
    cdef list data_list = byte2int(bitss, n_extended_bytes)
    cdef bytes previous = keys[data_list[0]]
    cdef list uncompressed = [previous]
    cdef int n_keys = 256
    cdef Integer i
    cdef bytes current
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

    cdef str unc = b"".join(uncompressed).decode()
    return unc