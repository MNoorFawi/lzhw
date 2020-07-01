cdef extern from "Python.h":
    char* PyUnicode_AsUTF8(object unicode)

cimport numpy as np
import numpy as np
from libc.stdlib cimport malloc#, free
from cpython cimport dict

ctypedef fused list_arr:
    list
    np.ndarray

cdef char ** to_c_string_list(str_list):
    cdef int l = len(str_list)
    cdef char **c_string = <char **>malloc(l * sizeof(char *))
    for i in range(l):
        c_string[i] = PyUnicode_AsUTF8(str_list[i])
    return c_string

#cdef int * to_c_int(a):
#    cdef int *ind_ints
#    ind_ints = <int *>malloc(len(a) * sizeof(int))
#    if ind_ints is NULL:
#        raise MemoryError()
#    for i in range(len(a)):
#        ind_ints[i] = a[i]
#    return ind_ints

cdef tuple update_dict(dict sb, char *v, int loc):
    cdef signed int buffer
    if v in sb:
        buffer = sb[v][-1]
        sb[v].append(loc)
    else:
        sb[v] = [loc]
        buffer = loc - 1
    return sb, buffer

cdef int get_buffer(list indices, int iter, int current_buffer):
    cdef signed int buffer
    if iter > len(indices):
        buffer = current_buffer - 1
    else:
        buffer = indices[-iter]
    return buffer

cdef tuple lz77compress(list dat, int sliding_window):
    l = len(dat)
    cdef char **data = to_c_string_list(dat)
    #cdef int _sliding_window = 256
    cdef int current_location = 0
    cdef dict search_buffer = {}
    cdef np.ndarray[dtype=object, ndim=1] triplets = np.empty(l, dtype=object)
    #cdef tuple triplet
    cdef int ols
    cdef signed int buffer
    cdef int i = 0
    #cdef list indx
    #cdef char *v

    while current_location < l:
        v = data[current_location]
        if v in search_buffer:
            buffer = search_buffer[v][-1]
            search_buffer[v].append(current_location)
        else:
            search_buffer[v] = [current_location]
            buffer = current_location - 1
        #search_buffer, buffer = update_dict(search_buffer, v, current_location)
        indx = search_buffer[v]
        triplet = triplet_encode(data, current_location, sliding_window, l, buffer, indx)
        triplets[i] = triplet
        i += 1
        if not triplet[1]:
            ols = 0
        else:
            ols = triplet[1]
        current_location += 1 + ols
    #free(data)
    return triplets, i

cdef tuple triplet_encode(char **data, int current_location, int sliding_window,
                          int l, int buffer_slide, list indices):
    cdef int _match_len = 0
    cdef int match_offset = 0
    cdef int buffer_start = current_location - buffer_slide
    cdef int matchlen
    cdef int iter = 2

    while buffer_slide >= 0 and buffer_start < sliding_window:
        matchlen = match(data, current_location, buffer_slide, l)
        if matchlen > _match_len:
            _match_len = matchlen
            match_offset = buffer_start
        iter += 1
        buffer_slide = get_buffer(indices, iter, buffer_slide)
        buffer_start = current_location - buffer_slide
        #buffer_slide
    if match_offset == 0:
        mo = None
        _ml = None
    else:
        mo = match_offset
        _ml = _match_len
    cdef char *literal = data[current_location + _match_len]
    return mo, _ml, literal

cdef int match(char **data, int current_location, int buffer_slide, int l):
    cdef int matchlen = 0
    while current_location + matchlen + 1 < l:
        if data[current_location + matchlen] != data[buffer_slide + matchlen]:
            break
        matchlen += 1
    return matchlen

cpdef np.ndarray lz77_compress(list data, int sliding_window = 256):
    tripletss = lz77compress(data, sliding_window)
    cdef np.ndarray triplet = tripletss[0]
    cdef int i = tripletss[1]
    cdef np.ndarray[dtype=object, ndim=1] compressed = triplet[:i]
    return compressed

cdef list lz77decompress(list_arr compressed, int n_rows):
    #cdef tuple triplet
    decompressed = []
    cdef int offset, length, current_location, i
    for triplet in compressed:
        literal = triplet[2]
        if isinstance(literal, bytes):
            literal = literal.decode()
        if isinstance(triplet[0], int):
            offset = triplet[0]
            length = triplet[1]
            current_location = len(decompressed) - offset
            if offset == 1:
                decompressed += [decompressed[current_location]] * length
                current_location += length
            else:
                for i in range(length):
                    decompressed.append(decompressed[current_location])
                    current_location += 1
        decompressed.append(literal)
        if n_rows > 0 and len(decompressed) >= n_rows:
            break
    return decompressed

cpdef np.ndarray lz77_decompress(list_arr compressed, int n_rows = 0):
    decompressed = lz77decompress(compressed, n_rows)
    cdef np.ndarray[dtype=object, ndim=1] arr = np.empty(len(decompressed), dtype=object)
    arr[:] = decompressed
    return arr

