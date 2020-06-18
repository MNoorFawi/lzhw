from lzw_c import *
from lz77c import lz77_decompress

def glue_seq(seq, last_separate = False):
    if last_separate:
        s = seq.split()
        return " ".join(s[:-1]), s[-1]
    else:
        return " ".join(seq)

def code_filling(huff_codes, n):
    sequences = {}
    codes = {}
    for seq, code in huff_codes.items():
        cd = int("1" + code, 2)
        if n == "literal_str":
            sequences[cd] = lzw_compress(str(seq))
        elif n == "literal":
            sequences[cd] = eval(seq) if seq != "nan" else seq
        else:
            sequences[cd] = seq
        codes[seq] = code
    return sequences, codes

def huffman_decode(sequences, compressed, n):
    bitstring = bin(compressed)[2:]
    bit = ""
    for b in bitstring[1:]:  # after preceding 1
        bit += b
        bit_int = int("1" + bit, 2)
        if bit_int in sequences:
            if n == "literal_str":
                org = lzw_decompress(sequences[bit_int])
            else:
                org = str(sequences[bit_int])
            yield org
            bit = ""

def org_shaping(seq, bits, n):
    org = " ".join(huffman_decode(seq, bits, n)).split()
    org = [i.replace("__", " ") for i in org]
    if "None" in org:
        org = [eval(i) for i in org]
    return org

def lz77_decode(triplets, n_rows):
    triplets = list(zip(triplets[0], triplets[1], triplets[2]))
    decomp = lz77_decompress(triplets, n_rows)
    return decomp

def lzhw_decompress(sequences, triplets, n_rows):
    if "lz77" in sequences:
        decomp = lz77_decode(triplets, n_rows)
    else:
        trplts = []
        for n, i in zip(sequences.keys(), range(len(triplets))):
            triplet = org_shaping(sequences[n], triplets[i], n)
            trplts.append(triplet)
        decomp = lz77_decode(trplts, n_rows)
    return decomp