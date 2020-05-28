from .lzw import *

def glue_seq(seq, last_separate = False):
    if last_separate:
        s = seq.split()
        return " ".join(s[:-1]), s[-1]
    else:
        return " ".join(seq)

def code_filling(huff_codes):
    sequences = {}
    codes = {}
    for seq, code in huff_codes.items():
        sequences[code] = lzw_compress(seq)
        codes[seq] = code
    return sequences, codes

def huffman_decode(sequences, compressed):
    bitstring = bin(compressed)[2:]
    bit = ""
    for b in bitstring[1:]:  # after preceding 1
        bit += b
        if bit in sequences:
            yield lzw_decompress(sequences[bit])
            bit = ""
