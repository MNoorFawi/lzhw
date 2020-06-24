#from lzw_c import *
from cpython cimport int as Integer
cimport numpy as np
import numpy as np


ctypedef fused list_arr:
    np.ndarray
    list

ctypedef fused str_tuple:
    tuple
    str

def cylistappend(list lst, x):
     cdef list result = lst[:]
     result.append(x)
     return result

cdef np.ndarray lz77compress(list_arr data):
    cdef int l = len(data)
    cdef int _sliding_window = 512
    cdef int current_location = 0
    cdef list triplets = []
    cdef tuple triplet
    cdef int ol
    cdef int ols
    while current_location < l:
        triplet = triplet_encode(data, current_location, _sliding_window)
        triplets.append(triplet)
        if not triplet[1]:
            ols = 0
        else:
            ols = triplet[1]
        current_location += 1 + ols
    cdef np.ndarray[dtype=object, ndim=1] arr = np.empty(len(triplets), dtype=object)
    arr[:] = triplets
    return arr

cdef tuple triplet_encode(list_arr data, int current_location, int sliding_window):
    cdef int _match_len = 0
    cdef int match_offset = 0
    cdef int buffer_start = 1
    cdef int buffer_slide = current_location - buffer_start
    cdef int matchlen
    while buffer_slide >= 0 and buffer_start < sliding_window:
        matchlen = match(data, current_location, buffer_slide)
        if matchlen > _match_len:
            _match_len = matchlen
            match_offset = buffer_start
        buffer_start += 1
        buffer_slide -= 1
    if match_offset == 0:
        mo = None
        _ml = None
    else:
        mo = match_offset
        _ml = _match_len
    literal = data[current_location + _match_len]
    #cdef Integer literal = lzw_compress(liter)
    return mo, _ml, literal

cdef int match(list_arr data, int current_location, int buffer_slide):
    cdef int matchlen = 0
    while current_location + matchlen + 1 < len(data):
        if data[current_location + matchlen] != data[buffer_slide + matchlen]:
            break
        matchlen += 1
    return matchlen

cpdef np.ndarray lz77_compress(list_arr data):
    cdef np.ndarray triplets = lz77compress(data)
    return triplets

cdef list lz77decompress(list_arr compressed, int n_rows):
    cdef tuple triplet
    #cdef str decomp
    cdef list decompressed = []
    cdef int l #= len(decompressed)
    cdef int offset #= int(triplet[0])
    cdef int length #= int(triplet[1)
    #cdef Integer liter #= triplet[2]
    #cdef str literal
    cdef int current_location #= l - offset
    cdef int i
    for triplet in compressed:
        if not triplet[0]:
            offset = 0
            length = 0
        else:
            offset = triplet[0]
            length = triplet[1]
        literal = triplet[2]
        #literal = lzw_decompress(liter)
        if offset > 0:
            l = len(decompressed)
            current_location = l - offset
            for i in range(length):
                decomp = decompressed[current_location]
                decompressed.append(decomp)
                current_location += 1
        decompressed.append(literal)
        if n_rows > 0 and len(decompressed) >= n_rows:
            break
    return decompressed

cpdef np.ndarray lz77_decompress(list_arr compressed, int n_rows = 0):
    cdef list decompressed = lz77decompress(compressed, n_rows)
    cdef np.ndarray[dtype=object, ndim=1] arr = np.empty(len(decompressed), dtype=object)
    arr[:] = decompressed
    return arr

