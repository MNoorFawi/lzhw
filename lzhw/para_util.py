from joblib import Parallel, delayed
from .lzhw_alg import LZHW
from tqdm import tqdm
from .compress_util import lzhw_decompress


def lzhw_para(df, selected, sliding_window, n_jobs):
    compressed = Parallel(n_jobs=n_jobs, max_nbytes=None, backend="multiprocessing")(delayed(
        LZHW)(list(df.iloc[:, i]), sliding_window) for i in tqdm(selected))
    return compressed

def para_decompress(sequences, triplets, n_rows, n_jobs):
    decompressed = Parallel(n_jobs=n_jobs, max_nbytes=None, backend="multiprocessing")(delayed(
        lzhw_decompress)(sequences[i], triplets[i], n_rows) for i in tqdm(range(len(sequences))))
    return decompressed
