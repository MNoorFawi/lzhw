# More Compression Functions

Aside from the functions and classes discussed, the library also has some more compression functions that can be used as standalone.

#### lz78()

**lz78** which performs the famous **lempel-ziv78** algorithm which differs from lempel-ziv77 in that instead of triplets it creates a dictionary for the previously seen sequences:
```python
import random
random.seed(1311)
example = random.choices(["A", "B", "C"], k = 20)
print(example)
#['A', 'A', 'C', 'C', 'A', 'A', 'C', 'C', 'C', 'B', 'B', 
# 'A', 'B', 'B', 'C', 'C', 'B', 'C', 'C', 'B']

import lzhw
lz78_comp, symb_dict = lzhw.lz78(example)
print(lz78_comp)
# ['1', '1', 'C', '3', '1', 'A', '3', 'C', '3', 'B', 
#  '7', '1', 'B', '7', 'C', '6', 'C', 'C B']

print(symb_dict)
# {'A': '1', 'A C': '2', 'C': '3', 'A A': '4', 'C C': '5', 
#  'C B': '6', 'B': '7', 'A B': '8', 'B C': '9', 'C B C': '10'}
```

#### huffman_coding()

Huffman Coding function which takes a Counter object and encodes each symbol accordingly.
```python
from collections import Counter
huffs = lzhw.huffman_coding(Counter(example))
print(huffs)
# {'A': '10', 'C': '0', 'B': '11'}
```

#### lzw_compress() and lzw_decompress()

They perform [lempel-ziv-welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) compressing and decompressing
```python
print(lzhw.lzw_compress("Hello World"))
# 723201696971929295664359987300

print(lzhw.lzw_decompress(lzhw.lzw_compress("Hello World")))
# Hello World
```

#### lz20()
I wanted to modify the lempel-ziv78 and instead of creating a dictionary and returing the codes in the output compressed stream, I wanted to glue the repeated sequences together to get a shorter list with more repeated sequences to further use it with huffman coding.

I named this function lempel-ziv20 :D:
```python
lz20_ex = lzhw.lz20(example)
print(lz20_ex)
# ['A', 'A', 'C', 'C', 'A', 'A', 'C', 'C', 'C', 'B', 'B', 
#  'A', 'B', 'B', 'C', 'C B', 'C', 'C B']

huff20 = lzhw.huffman_coding(Counter(lz20_ex))
print(huff20)
# {'A': '10', 'C': '0', 'B': '111', 'C B': '110'}
```

In data with repeated sequences it will give better huffman dictionaries.

#### lz77_compress() and lz77_decompress()

The main two functions in the library which apply the lempel-ziv77 algorithm:

```python
lz77_ex = lzhw.lz77_compress(example)
print(lz77_ex)
# [(None, None, 'A'), (1, 1, 'C'), (1, 1, 'A'), (4, 3, 'C'), 
#  (None, None, 'B'), (1, 1, 'A'), (3, 2, 'C'), (7, 2, 'C'), (1, 1, 'B')]

lz77_decomp = lzhw.lz77_decompress(lz77_ex)
print(lz77_decomp == example)
# True
```

Also we can selected how many elements we want to decompress from the original list instead of decompressing it all:

```python
print(lzhw.lz77_decompress(lz77_ex, 3))
#['A', 'A', 'C']
```