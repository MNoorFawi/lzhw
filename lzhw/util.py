from math import ceil

def bit_fill(comp):
    return "".join([bin(i)[2:].zfill(9) for i in comp])

def byte_encode(bits):
    return int(bits, 2).to_bytes(ceil(len(bits) / 8), "big")

def byte_decode(enc):
    return bin(int.from_bytes(enc, "big"))[2:].zfill(len(enc) * 8)

def byte2int(bits, ext_bytes):
    return [int(bits[i * 9:(i + 1) * 9], 2) for i in range(ext_bytes)]

ascii_to_int = {i.to_bytes(1, "big"): i for i in range(256)}
int_to_ascii = {i: b for b, i in ascii_to_int.items()}
