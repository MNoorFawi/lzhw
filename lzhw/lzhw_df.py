from .lzhw_alg import LZHW
from pickle import dump, load, HIGHEST_PROTOCOL
from .compress_util import lz77_decode, org_shaping
import pandas as pd
from lzw_c import *
from tqdm import tqdm
from operator import itemgetter

class CompressedDF:
    def __init__(self, df, selected_cols = "all"):
        #self.columns = list(df.columns)
        if selected_cols == "all":
            selected = range(df.shape[1])
        else:
            selected = selected_cols
        self.columns = list(itemgetter(*selected)(df.columns))
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
            if any(isinstance(c, str) for c in selected_cols):
                selected_cols = [i for i, v in enumerate(cols) if v in selected_cols]
            selected = selected_cols
        df = {}
        for i in tqdm(range(len(cols))):
            triplets = load(input)
            sequences = load(input)
            if i not in selected:
                continue
            else:
                if "lz77" in sequences:
                    df[cols[i]] = lz77_decode(triplets)
                else:
                    triplts = []
                    for n, t in zip(sequences.keys(), range(len(triplets))):
                        triplet = org_shaping(sequences[n], triplets[t])
                        triplts.append(triplet)
                    df[cols[i]] = lz77_decode(triplts)

    return pd.DataFrame(df)
