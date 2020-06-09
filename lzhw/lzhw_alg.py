from collections import Counter
from sys import getsizeof
from pickle import dump, load, HIGHEST_PROTOCOL
from lz77c import lz77_compress
from .huffman_coding import huffman_coding
from .compress_util import lz77_decode, code_filling, org_shaping
from lzw_c import *

# Putting everything together in one class
# Lempel-Ziv-Huffman-Welch. I invented it :D
class LZHW:
    def __init__(self, uncompressed):
        self._compress(uncompressed)

    def _compress(self, uncompressed):
        self.__original_size = getsizeof(uncompressed)
        uncompressed = list(map(str, uncompressed))
        lz77_triplets = lz77_compress(uncompressed)
        if len(lz77_triplets) / len(uncompressed) >= 1.5:
            self.sequences = {"lz77": True}
            self.compressed = list(zip(*lz77_triplets))
        else:
            lz77_list = list(zip(*lz77_triplets))
            self.sequences = {}
            self.__codes = {}
            names = [lzw_compress(n) for n in ["offset", "length", "literal"]]
            for n, l in zip(names, lz77_list):
                seq_freq = dict(Counter(l))
                huff_coding = huffman_coding(seq_freq)
                self.sequences[n], self.__codes[n] = code_filling(huff_coding)
            self.compressed = tuple([self.__encode(t, n) for t, n in zip(lz77_list, names)])

    def __encode(self, triplets, n):
        # adding preceding 1 to ensure not losing preceding binary 0s
        bitstring = "1" + "".join(self.__codes[n][seq] for seq in triplets)
        # saving compressed object as an integer from the bit string to save more space
        return int(bitstring, 2)

    def decompress(self):
        if "lz77" in self.sequences:
            decomp = lz77_decode(self.compressed)
        else:
            triplets = []
            for n, i in zip(self.sequences.keys(), range(len(self.compressed))):
                triplet = org_shaping(self.sequences[n], self.compressed[i])
                triplets.append(triplet)
            decomp = lz77_decode(triplets)
        return decomp

    def size(self):
        return getsizeof(self.compressed)

    def space_saving(self):
        return "space saving from original to compressed is {}%".format(
            round((1 - (self.size() / self.__original_size)) * 100), 2)

    def save_to_file(self, file):
        with open(file, "wb") as output:
            dump(self.compressed, output, HIGHEST_PROTOCOL)
            dump(self.sequences, output, HIGHEST_PROTOCOL)

def decompress_from_file(file):
    with open(file, "rb") as input:
        triplets = load(input)
        sequences = load(input)

    if "lz77" in sequences:
        original = lz77_decode(triplets)
    else:
        triplts = []
        for n, i in zip(sequences.keys(), range(len(triplets))):
            triplet= org_shaping(sequences[n], triplets[i])
            triplts.append(triplet)
        original = lz77_decode(triplts)

    return original
