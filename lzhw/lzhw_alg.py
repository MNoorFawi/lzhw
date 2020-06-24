from collections import Counter
from sys import getsizeof
from pickle import dump, load, HIGHEST_PROTOCOL
from lz77c import lz77_compress
from .huffman_coding import huffman_coding
from .compress_util import lzhw_decompress, code_filling
from .util import is_number
import numpy as np

# Putting everything together in one class
# Lempel-Ziv-Huffman-Welch. I invented it :D
class LZHW:
    def __init__(self, uncompressed):
        self._compress(uncompressed)

    def _compress(self, uncompressed):
        self.__original_size = getsizeof(uncompressed)
        is_num = is_number(uncompressed[0])
        if not isinstance(uncompressed, np.ndarray):
            uncompressed = np.array(uncompressed)
        if len(set(uncompressed)) / len(uncompressed) >= 0.8:
            self.sequences = {"lz77": True}
            self.compressed = uncompressed
        else:
            uncompressed = [i.replace(" ", "__") for i in map(str, uncompressed)]
            #uncompressed = uncompressed.astype(str)
            #uncompressed = np.char.replace(uncompressed, " ", "__")
            lz77_triplets = lz77_compress(uncompressed)
            #if len(lz77_triplets) / len(uncompressed) >= 1.5: # this is a placeholder for future
                                                              # enhancement for data with no repeated sequences
            #    self.sequences = {"lz77": True}
            #    self.compressed = list(zip(*lz77_triplets))
            #else:
            lz77_list = list(zip(*lz77_triplets))
            self.sequences = {}
            self.__codes = {}
            if is_num:
                names = ["offset", "length", "literal"]
            else:
                names = ["offset", "length", "literal_str"]
            for n, l in zip(names, lz77_list):
                seq_freq = dict(Counter(l))
                huff_coding = huffman_coding(seq_freq)
                self.sequences[n], self.__codes[n] = code_filling(huff_coding, n)
            self.compressed = tuple([self.__encode(t, n) for t, n in zip(lz77_list, names)])

    def __encode(self, triplets, n):
        # adding preceding 1 to ensure not losing preceding binary 0s
        bitstring = "1" + "".join(self.__codes[n][seq] for seq in triplets)
        # saving compressed object as an integer from the bit string to save more space
        return int(bitstring, 2)

    def decompress(self, n_rows = 0):
        decomp = lzhw_decompress(self.sequences, self.compressed, n_rows)
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

def decompress_from_file(file, n_rows = 0):
    with open(file, "rb") as input:
        triplets = load(input)
        sequences = load(input)

    original = lzhw_decompress(sequences, triplets, n_rows)
    return original
