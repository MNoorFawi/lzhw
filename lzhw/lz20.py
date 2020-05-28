from .compress_util import glue_seq

def lz20(data):
    """Lempel-Ziv 2020 :D using the naming convention of lz77 and lz78.
       The idea of the algorithm that it looks for sequences in the data as in lz78.
       But instead of creates the dictionary and assigning codes while compressing,
       it glues the sequences together for the huffman coding to code them based on occurrences."""

    data = list(map(str, data))
    data = [i.replace(" ", "---") for i in data]
    i = 1
    sequences = []
    start = 0
    n_data = len(data)
    seq_dict = {}

    while i <= n_data:
        s = glue_seq(data[start:i])
        ls = len(s.split())
        if s in seq_dict:
            if ls + start >= n_data:
                # if it is the final seq just append it
                sequences.append(s)
                seq_dict[s] += 1
                break  # ensure that it doesn't loop forever
            seq_dict[s] += 1
            i += 1
            continue
        else:
            seq_dict[s] = 1
            if " " in s:  # it is a sequence of symbols not one symbol
                h, t = glue_seq(s, last_separate = True)
                sequences.append(h)
                sequences.append(t)
            else:
                sequences.append(s)
            start += ls
            i += 1

    return sequences
