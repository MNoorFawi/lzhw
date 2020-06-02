ctypedef fused str_or_list:
    list
    str

ctypedef fused int_str:
    int
    str

cdef tuple[str] glue_seq_s(str_or_list seq):
    cdef list s = seq.split()
    cdef str h = " ".join(s[:-1])
    cdef str t = s[-1]
    #cdef bytes hb = h.encode()
    #cdef char* hc = hb
    return h, t
		
cdef str glue_seq_l(str_or_list seq):
    cdef str hs = " ".join(seq)
    return hs

cdef list lz20_c(list data):
    data = list(map(str, data))
    cdef str ch
    data = [ch.replace(" ", "---") for ch in data]
    cdef int i = 1
    cdef list sequences = []
    cdef list dst
    cdef int start = 0
    cdef int n_data = len(data)
    cdef dict seq_dict = {}
    cdef str h, t, s
    cdef int ls
    
    while i <= n_data:
        dst = data[start:i]
        s = glue_seq_l(dst)
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
                h, t = glue_seq_s(s)
                sequences.append(h)
                sequences.append(t)
            else:
                sequences.append(s)
            start += ls
            i += 1

    return sequences

cpdef list lz20(list uncomp):
    cdef list comp = lz20_c(uncomp)
    return comp
