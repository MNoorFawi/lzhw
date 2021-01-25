# lzhw (DataFrame Compression)

**Compression library for data frames and tabular data files, csv, excel etc.**

![lzhw logo](./img/lzhw_logo.jpg)

[![Build Status](https://travis-ci.com/MNoorFawi/lzhw.svg?branch=master)](https://travis-ci.com/MNoorFawi/lzhw)

**Compression** library to compress big lists and/or pandas dataframes using an **optimized algorithm (lzhw)** developed from Lempel-Ziv, Huffman and LZ-Welch techniques.

**The library supports parallelism and most of its core code is written in Cython so it is quite fast.**

**lzhw has a command line tool that can be downloaded from [here](https://github.com/MNoorFawi/lzhw/releases/download/v0.0.10/lzhw.exe) and can work from command line with no prior python installation.**

**Manual on how to use it available [here](https://mnoorfawi.github.io/lzhw/5%20Using%20the%20lzhw%20command%20line%20tool/)**.

It works on Windows and soon a Mac version will be available.

## How lzhw Works

#### Overview
The library's main goal is to compress data frames, excel and csv files so that they consume less space to overcome memory errors.
Also to enable dealing with large files that can cause memory errors when reading them in python or that cause slow operations.
With **lzhw**, we can read compressed files and do operations **column by column**  and **on specific rows** only on chunks that we are interesred in. 

The algorithm is a mix of the famous **lempel-ziv and huffman coding** algorithm with some use of **lempel-ziv-welch** algorithm.

**lzhw** uses [**lempel-ziv77**](https://en.wikipedia.org/wiki/LZ77_and_LZ78) to discover repeated sequences in the stream and construct *triplets*, in that format <**offset,length,literal**>. 
Where *offset* is how many steps should we return back word to find the beginning of the current sequence and *length* is how many steps should we move and *literal* is the next value after the sequence.

Then we will have 3 shorter lists representing the stream, where [**Huffman Coding**](https://en.wikipedia.org/wiki/Huffman_coding) can come to the game encoding them.
.Huffman will produce code dictionaries

Then [Lempel-Ziv-Welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch), **lzw_compress()**, is used to further compress these dictionaries produces by Huffman. 

#### DEFLATE Note
The techniques may seem similar to the [**DEFLATE**](https://en.wikipedia.org/wiki/DEFLATE) algorithm which uses both LZSS, which is a variant of LZ77, and huffman coding, but I am not sure how the huffman coding further compresses the triplets. I believe it compresses the triplets altogether not as 3 separate lists as lzhw.
 And also it doesn't use the lempel-ziv-welch for further compression.

LZHW also uses a **modified version of LZ77**, in which it uses a dictionary, **key-value data structure, to store the already-seen patterns with their locations during the compression process, so that the algorithm instead of blindly going back looking for matching, it knows where exactly to go**. This **speeds up the compression process**.

For example, let's say the algorithm now has found "A", it needs to see in previous sequences where is the longest match. It will do so using the dictionary {"A": [1, 4, 5, 8]}. So it will go and start looking starting from these locations instead of blindly looking for "A"'s indices. 

DEFLATE Algorithm may be more complicated than lzhw, discussed here, but the latter is designed specifically for **tabular data** types to help in **data science** and **data analysis** projects.

#### Putting all together with LZHW Class
All of the steps can be done at once using **LZHW** class as follows and as shown in the Quick Start section:
```python
import lzhw
import sys

example = ["to", "be", "or", "not", "to", "be", "or", "to", "be", "or", "not"] * 4
lzhw_comp = lzhw.LZHW(example)
print(lzhw_comp.compressed)
# (8012, 8012, 15532) # this is how the compressed data looks like and stored

print(lzhw_comp.sequences) 
# {'offset': {3: None, 10: 4, 11: 7, 4: 11}, 
#  'length': {3: None, 10: 3, 11: 6, 4: 28}, 
#  'literal_str': {7: 321647, 12: 312421, 13: 319090, 2: 163110516}}
```
**Compressed data is now a tuple of three integers and a dictionary of three keys**. All values are integers not string for better space saving.

```python
print(sys.getsizeof(example)) 
print(sys.getsizeof(lzhw_comp.sequences) + sys.getsizeof(lzhw_comp.compressed))
# 416
# 312
```
The compressed tuple and the dictionary sizes are smaller than the original. Try to increase the 4 by which the list is multiplied, you will find that this 312 will never change.
