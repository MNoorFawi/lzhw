from .lzhw_alg import LZHW
from pickle import dump, load, HIGHEST_PROTOCOL
from .compress_util import huffman_decode
import pandas as pd

class CompressedDF:
    def __init__(self, df, selected_columns = "all"):
        self.columns = df.columns
        if selected_columns == "all":
            selected = range(df.shape[1])
        else:
            selected = selected_columns
        self.compressed = []
        for i in selected:
            comp_col = LZHW(df.iloc[:, i])
            self.compressed.append(comp_col)

    def save_to_file(self, file):
        with open(file, "wb") as output:
            dump(self.columns, output, HIGHEST_PROTOCOL)
            for i in range(len(self.columns)):
                dump(self.compressed[i].compressed, output, HIGHEST_PROTOCOL)
                dump(self.compressed[i].sequences, output, HIGHEST_PROTOCOL)

def decompress_df_from_file(file):
    with open(file, "rb") as input:
        cols = load(input)
        df = {}
        for i in range(len(cols)):
            bit_string = load(input)
            sequences = load(input)
            df[cols[i]] = " ".join(huffman_decode(sequences, bit_string)).split()
    return pd.DataFrame(df)