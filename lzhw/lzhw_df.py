from .lzhw_alg import LZHW
from pickle import dump, load, HIGHEST_PROTOCOL
from .compress_util import huffman_decode, org_shaping
import pandas as pd
from lzw_c import *
from tqdm import tqdm

class CompressedDF:
    def __init__(self, df, selected_cols = "all"):
        self.columns = list(df.columns)
        if selected_cols == "all":
            selected = range(df.shape[1])
        else:
            selected = selected_columns
        self.compressed = []
        for i in tqdm(selected):
            comp_col = LZHW(list(df.iloc[:, i]))
            self.compressed.append(comp_col)

    def save_to_file(self, file):
        with open(file, "wb") as output:
            cols = [i.replace(" ", "__") for i in self.columns]
            dump(lzw_compress(" ".join(cols)), output, HIGHEST_PROTOCOL)
            for i in range(len(self.columns)):
                dump(self.compressed[i].compressed, output, HIGHEST_PROTOCOL)
                dump(self.compressed[i].sequences, output, HIGHEST_PROTOCOL)

def decompress_df_from_file(file, selected_cols = "all"):
    with open(file, "rb") as input:
        cols = load(input)
        cols = lzw_decompress(cols).split()
        cols = [i.replace("__", " ") for i in cols]
        if selected_cols == "all":
            selected = range(len(cols))
        else:
            selected = selected_cols
        df = {}
        for i in tqdm(range(len(cols))):
            bit_string = load(input)
            sequences = load(input)
            if i in selected:
                df[cols[i]] = org_shaping(sequences, bit_string)
            else:
                continue
    return pd.DataFrame(df)
