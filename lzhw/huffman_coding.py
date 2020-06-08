from .pq import CodeHeap

def huffman_coding(symb2freq):
    """Huffman coding to encode symbols/sequences.
    It takes the Counter of Compressed object and
    returns a code dictionary based on occurences"""

    if len(symb2freq) == 1:
        symb = list(symb2freq.keys())[0]
        return {symb: '0'}

    symb_code_queue = CodeHeap()
    code_dict = {symbs: "" for symbs in symb2freq}

    for symbs, freq in symb2freq.items():
        if not symbs:
            symbs = 0
        if not freq:
            freq = 0
        symb_code_queue.push((freq, [symbs]))

    while len(symb_code_queue) > 1:
        low_freq, low_symbs = symb_code_queue.pop()
        high_freq, high_symbs = symb_code_queue.pop()

        for symb in low_symbs:
            if symb == 0:
                symb = None
            code_dict[symb] = "0" + code_dict[symb]
        for symb in high_symbs:
            if symb == 0:
                symb = None
            code_dict[symb] = "1" + code_dict[symb]

        symb_code_queue.push(
            (low_freq + high_freq,
             sorted(low_symbs + high_symbs)
             )
        )

    return code_dict
