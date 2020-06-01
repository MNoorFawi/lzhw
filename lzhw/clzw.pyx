cdef str char(int x):
    cdef str c = chr(x)
    return c

cdef list ccompress(str uncompressed):

    cdef list result = []
    cdef int dict_size = 256
    cdef int i
    cdef dict dictionary = {char(i): i for i in range(dict_size)}

    cdef str w = ""
    cdef str c, wc
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result

cpdef list compress(str ccompressed):
    cdef list pycomp = ccompress(ccompressed)
    return pycomp