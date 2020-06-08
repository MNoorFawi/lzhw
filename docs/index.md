# lzhw (DataFrame Compression)
##### Compression library for data frames and tabular data files, csv,excel etc.

[![Build Status](https://travis-ci.com/MNoorFawi/lzhw.svg?branch=master)](https://travis-ci.com/MNoorFawi/lzhw)

**Compression** library to compress big lists and/or pandas dataframes using an **optimized algorithm (lzhw)** developed from Lempel-Ziv, Huffman and LZ-Welch techniques.

## How lzhw Works
The library's main goal is to compress data frames, excel and csv files so that they consume less space to overcome memory errors.
Also to enable dealing with large files that can cause memory errors when reading them in python or that cause slow operations.
With **lzhw**, we can read compressed files and do operations **column by column** only on columns that we are interesred in. 

The algorithm is a mix of the famous **lempel-ziv and huffman coding** algorithm with some use of **lempel-ziv-welch** algorithm.
The algorithm starts with an input stream for example this one:
```python
example = ["to", "be", "or", "not", "to", "be", "or", "to", "be", "or", "not"] * 2
print("".join(example))
# tobeornottobeortobeornottobeornottobeortobeornot
```
**lzhw** uses [**lz77**](https://en.wikipedia.org/wiki/LZ77_and_LZ78) to discover repeated sequences in the stream and construct *triplets*, in that format **<offset,length,literal>** where *offset* is how many steps should we return back word to find the beginning of the current sequence and *length* is how many steps should we move and *literal* is the next value after the sequence.

Then we will have 3 shorter lists representing the stream, where [**Huffman Coding**](https://en.wikipedia.org/wiki/Huffman_coding) can come to the game encoding them.

The function that performs lempel-ziv and returning the triplets called **lz77_compress**.
```python
import lzhw
lz77_ex = lzhw.lz77_compress(example)
print(lz77_ex)
# [(None, None, 321647), (None, None, 312421), (None, None, 319090), 
#  (None, None, 163110516), (4, 3, 321647), (7, 6, 163110516), (11, 6, 163110516)]
```
Here all the **None**s values are originally "0s" but converted to None to save more space.
The third item in each tuple is originally a string from the input stream but was compressed using **lzw_compress** function which applies [lempel-ziv-welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) compression and stores the values as integer instead of original string for **extra space saving**.

Now huffman coding will take the offsets list, lengths list and literal list and encode them based on most occurring values to give:
```python
lz77_lists = list(zip(*lz77_ex))
print(lz77_lists)
# [(None, None, None, None, 4, 7, 11), (None, None, None, None, 3, 6, 6), 
#  (321647, 312421, 319090, 163110516, 321647, 163110516, 163110516)]

huffs = []
from collections import Counter
for i in range(len(lz77_lists)):
    huff = lzhw.huffman_coding(Counter(lz77_lists[i]))
    huffs.append(huff)
print(huffs)
# [{None: '1', 4: '010', 7: '011', 11: '00'}, {None: '1', 3: '00', 6: '01'}, 
#  {321647: '11', 312421: '100', 319090: '101', 163110516: '0'}]
```
Now if we encode each value in the triplets with its corresponding value from the huffman dictionary and append everything together we will have:
```python
bits = []
for i in range(len(huffs)):
    bit = "".join([huffs[i].get(k) for k in lz77_lists[i]])
    bits.append(bit)
print(bits)
# ['111101001100', '1111000101', '1110010101100']

print(len("".join(bits)))
# 35
```
Which has a length of **35** bits only!
 
Using each algorithm alone can give us bigger number of bits, for example, using only huffman coding will give us:
```python
huff_alone = lzhw.huffman_coding(Counter(example))
print(huff_alone)
# {'to': '11', 'be': '01', 'or': '10', 'not': '00'}

huff_bit = "".join([huff_alone.get(k) for k in example])
print(huff_bit)
# 11011000110110110110001101100011011011011000

print(len(huff_bit))
# 44
```
44 bits, 9 more bit!!! Big deal when dealing with bigger data.

The techniques may seem similar to the [**DEFLATE**](https://en.wikipedia.org/wiki/DEFLATE) algorithm which uses both lempel-ziv77 and huffman coding, but I am not sure how the huffman coding further compresses the triplets. And also it doesn't use the lempel-ziv-welch for further compression.

All of the steps can be done at once using **LZHW** class as follows and as shown in the Quick Start section:
```python
lzhw_comp = lzhw.LZHW(example)
print(lzhw_comp.compressed)
# (8012, 1989, 15532) # this is how the compressed data looks like and stored

print(lzhw_comp.sequences) # dictionary's keys and values are stored as integers as well
# {21926886918376052: {3: 79217613925, 10: 564, 11: 567, 4: 287281}, 
#  21821266153236584: {3: 79217613925, 4: 563, 5: 566}, 
#  11172629419993383532: {7: 19812244050700343, 12: 19812175464916017, 
#                        13: 38695657038082, 2: 5175286287971861424896}}
```