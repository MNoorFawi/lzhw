from collections import Counter
from sys import getsizeof
from pickle import dump, load, HIGHEST_PROTOCOL
from .lz20 import lz20
from .huffman_coding import huffman_coding
from .compress_util import code_filling, huffman_decode

# Putting everything together in one class
# Lempel-Ziv-Huffman-Welch. I invented it :D
class LZHW:
    def __init__(self, uncompressed):
        self._compress(uncompressed)

    def _compress(self, uncompressed):
        self.__original_size = getsizeof(uncompressed)
        lz20_sequences = lz20(uncompressed)
        seq_freq = Counter(lz20_sequences)
        huff_coding = huffman_coding(seq_freq)
        self.sequences, self.__codes = code_filling(huff_coding)
        self.compressed = self.__encode(lz20_sequences)

    def __encode(self, sequences):
        # adding preceding 1 to ensure not losing preceding binary 0s
        bitstring = "1" + "".join(self.__codes[seq] for seq in sequences)
        # saving compressed object as an integer from the bit string to save more space
        return int(bitstring, 2)

    def decompress(self):
        return " ".join(huffman_decode(self.sequences, self.compressed)).split()

    def size(self):
        return getsizeof(self.compressed)

    def space_saving(self):
        return "space saving from original to compressed is {}%".format(
            round((1 - (self.size() / self.__original_size)) * 100), 2)

    def save_to_file(self, file):
        with open(file, "wb") as output:
            dump(self.compressed, output, HIGHEST_PROTOCOL)
            dump(self.sequences, output, HIGHEST_PROTOCOL)

    def __repr__(self):
        return bin(self.compressed)[2:]

def decompress_from_file(file):
    with open(file, "rb") as input:
        bit_string = load(input)
        sequences = load(input)
    return " ".join(huffman_decode(sequences, bit_string)).split()