from .compress_util import glue_seq

def lz78(data):
    """Normal Lempel-Ziv78 which assigns codes for each new encountered sequence."""

    data = list(map(str, data))
    i = 1
    sequences = []
    start = 0
    n_data = len(data)
    seq_dict = {}
    code = 1

    while i <= n_data:
        s = glue_seq(data[start:i])
        ls = len(s.split())
        if s in seq_dict:
            if ls + start >= n_data:
                sequences.append(s)
                break
            i += 1
            continue
        else:
            seq_dict[s] = str(code)
            if " " in s:
                h, t = glue_seq(s, last_separate = True)
                sequences.append(seq_dict[h])
                sequences.append(t)
            else:
                sequences.append(seq_dict[s])
            start += ls
            i += 1
            code += 1

    return sequences, seq_dict
