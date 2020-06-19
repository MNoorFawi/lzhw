from joblib import Parallel, delayed
from .lzhw_alg import LZHW
from tqdm import tqdm
from .compress_util import lzhw_decompress

def lzhw_para(df, selected):
    compressed = Parallel(n_jobs=-1, max_nbytes = None)(delayed(
        LZHW)(list(df.iloc[:, i])) for i in tqdm(selected))
    return compressed

def para_decompress(sequences, triplets, n_rows):
    decompressed = Parallel(n_jobs=-1, max_nbytes = None)(delayed(
        lzhw_decompress)(sequences[i], triplets[i], n_rows) for i in tqdm(range(len(sequences))))
    return decompressed
