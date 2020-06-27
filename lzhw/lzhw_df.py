from .lzhw_alg import LZHW
from pickle import dump, load, HIGHEST_PROTOCOL
from .compress_util import _reader, lzhw_decompress
import pandas as pd
from lzw_c import *
from operator import itemgetter
from .para_util import lzhw_para, para_decompress
from tqdm import tqdm


class CompressedDF:
    def __init__(self, df, selected_cols="all", parallel=False, n_jobs=2):
        if selected_cols == "all":
            selected = range(df.shape[1])
        else:
            selected = selected_cols
        self.columns = list(itemgetter(*selected)(df.columns))
        if parallel:
            self.compressed = lzhw_para(df, selected, n_jobs)
        else:
            self.compressed = []
            for i in tqdm(selected):
                comp_col = LZHW(df.iloc[:, i].values)
                self.compressed.append(comp_col)

    def save_to_file(self, file):
        with open(file, "wb") as output:
            cols = [i.replace(" ", "__") for i in self.columns]
            dump(lzw_compress(" ".join(cols)), output, HIGHEST_PROTOCOL)
            for i in range(len(self.columns)):
                dump(self.compressed[i].compressed, output, HIGHEST_PROTOCOL)
                dump(self.compressed[i].sequences, output, HIGHEST_PROTOCOL)


def decompress_df_from_file(file, selected_cols="all", n_rows=0,
                            parallel=False, n_jobs=2,
                            selected_chunks = "all"):
    with open(file, "rb") as input:
        primer = load(input)

        if not isinstance(primer, int) and "__Chunks" in primer:
            def decompress_chunks(selected_chunks, parallel, n_jobs):
                dfs = {}
                total_chunks = primer["__Chunks"]
                if selected_chunks == "all":
                    sel_chunks = range(total_chunks)
                else:
                    sel_chunks = selected_chunks

                for ch in range(total_chunks):
                    chunk = load(input)
                    sc = list(chunk.keys())[0]
                    if sc not in sel_chunks:
                        continue
                    else:
                        cols = chunk[sc]["cols"]
                        cols = lzw_decompress(cols).split()
                        cols = [i.replace("__", " ") for i in cols]
                        triplets = []
                        sequences = []
                        for col in cols:
                            triplets.append(chunk[sc][col][0])
                            sequences.append(chunk[sc][col][1])
                        if parallel:
                            decompressed = para_decompress(sequences, triplets, n_rows, n_jobs)
                        else:
                            decompressed = []
                            for i in tqdm(range(len(sequences))):
                                decompressed.append(lzhw_decompress(sequences[i], triplets[i], n_rows))
                        df = dict(zip(cols, decompressed))

                        if n_rows > 0:
                            df = {k: v[:n_rows] for k, v in df.items()}
                        df = pd.DataFrame(df)
                        dfs[sc] = df
                return dfs
            return decompress_chunks(selected_chunks, parallel, n_jobs)

        else:
            cols = primer
            cols = lzw_decompress(cols).split()
            cols = [i.replace("__", " ") for i in cols]
            if selected_cols == "all":
                selected = range(len(cols))
            else:
                if any(isinstance(c, str) for c in selected_cols):
                    selected_cols = [i for i, v in enumerate(cols) if v in selected_cols]
                selected = selected_cols
            sequences, triplets = _reader(input, len(cols), selected)
            if parallel:
                decompressed = para_decompress(sequences, triplets, n_rows, n_jobs)
            else:
                decompressed = []
                for i in tqdm(range(len(sequences))):
                    decompressed.append(lzhw_decompress(sequences[i], triplets[i], n_rows))
            names = list(itemgetter(*selected)(cols))
            df = dict(zip(names, decompressed))

            if n_rows > 0:
                df = {k: v[:n_rows] for k, v in df.items()}
            df = pd.DataFrame(df)
            return df


class CompressedFromCSV:
    def __init__(self, file, header=0, chunksize=1e6,
                 selected_cols="all", parallel=False):
        self.all_comp = {}
        self.chunk_ind = 0
        for chunk in pd.read_csv(file, chunksize=chunksize, header=header):
            self._update_dict(self.chunk_ind, chunk, selected_cols, parallel)
            self.chunk_ind += 1
        print(f"File was compressed in {self.chunk_ind} chunk(s)")

    def _update_dict(self, new_ind, chunk, selected_cols, parallel):
        print(f"Compressing Chunk {new_ind} ...")
        self.all_comp[new_ind] = CompressedDF(chunk, selected_cols, parallel=parallel)

    def save_to_file(self, file, chunks = "all"):
        with open(file, "wb") as o:
            dump({"__Chunks": self.chunk_ind}, o, HIGHEST_PROTOCOL)
            if chunks == "all":
                selected = range(self.chunk_ind)
            else:
                selected = chunks

            if self.chunk_ind == 1:
                sel_chunks = [0]
            else:
                sel_chunks = list(itemgetter(*selected)(list(self.all_comp.keys())))

            for k in sel_chunks:
                to_be_dumped = {}
                cdf = self.all_comp[k]
                cdf_d = {}
                cols = [i.replace(" ", "__") for i in cdf.columns]
                cdf_d["cols"] = lzw_compress(" ".join(cols))
                for i in range(len(cols)):
                    cdf_d[cols[i]] = [cdf.compressed[i].compressed, cdf.compressed[i].sequences]
                to_be_dumped[k] = cdf_d
                dump(to_be_dumped, o, HIGHEST_PROTOCOL)
