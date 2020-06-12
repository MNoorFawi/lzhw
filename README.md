# lzhw
##### Compression library for data frames and tabular data files, csv, excel etc.

[![](https://img.shields.io/badge/docs-latest-blue.svg)](https://mnoorfawi.github.io/lzhw/) 
[![Build Status](https://travis-ci.com/MNoorFawi/lzhw.svg?branch=master)](https://travis-ci.com/MNoorFawi/lzhw)

**Compression** library to compress big lists and/or pandas dataframes using an **optimized algorithm (lzhw)** developed from Lempel-Ziv, Huffman and LZ-Welch techniques.

#### Full documentation can be found [here](https://mnoorfawi.github.io/lzhw/)

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
**lzhw** uses [**lempel-ziv77**](https://en.wikipedia.org/wiki/LZ77_and_LZ78) to discover repeated sequences in the stream and construct *triplets*, in that format **<offset,length,literal>**. 
Where *offset* is how many steps should we return back word to find the beginning of the current sequence and *length* is how many steps should we move and *literal* is the next value after the sequence.

Then we will have 3 shorter lists representing the stream, where [**Huffman Coding**](https://en.wikipedia.org/wiki/Huffman_coding) can come to the game encoding them.

The function that performs lempel-ziv and returning the triplets called **lz77_compress**.
```python
import lzhw
lz77_ex = lzhw.lz77_compress(example)
print(lz77_ex)
# [(None, None, 'to'), (None, None, 'be'), (None, None, 'or'), 
# (None, None, 'not'), (4, 3, 'to'), (7, 6, 'not'), (11, 6, 'not')]
```
Here all the **None**s values are originally "0s" but converted to None to save more space.

Now huffman coding will take the offsets list, lengths list and literal list and encode them based on most occurring values to give:
```python
lz77_lists = list(zip(*lz77_ex))
print(lz77_lists)
# [(None, None, None, None, 4, 7, 11), 
#  (None, None, None, None, 3, 6, 6), 
#  ('to', 'be', 'or', 'not', 'to', 'not', 'not')]

huffs = []
from collections import Counter
for i in range(len(lz77_lists)):
    huff = lzhw.huffman_coding(Counter(lz77_lists[i]))
    huffs.append(huff)
print(huffs)
# [{None: '1', 4: '010', 7: '011', 11: '00'}, {None: '1', 3: '00', 6: '01'}, 
#  {'to': '11', 'be': '100', 'or': '101', 'not': '0'}]
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

print(lzhw_comp.sequences) 
# {'offset': {3: None, 10: 4, 11: 7, 4: 11}, 
#  'length': {3: None, 4: 3, 5: 6}, 
#  'literal': {7: 'to', 12: 'be', 13: 'or', 2: 'not'}}
```

## Quick Start

```bash
pip install lzhw
```

```python
import lzhw

sample_data = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", 
               "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain", 
               "Rain", "Rain", "Sunny", "Sunny", "Overcaste"]

compressed = lzhw.LZHW(sample_data)
## let's see how the compressed object looks like:
print(compressed.compressed)
# (506460, 128794, 112504)

## its size
print(compressed.size())
# 72

## size of original
from sys import getsizeof
print(getsizeof(sample_data))
# 216

print(compressed.space_saving())
# space saving from original to compressed is 67%

## Let's decompress and check whether there is any information loss
decomp = compressed.decompress()
print(decomp == sample_data)
# True
```

As we saw, the LZHW class has saved 67% of the space used to store the original list without any loss. This percentage can get better with bigger data that may have repeated sequences.
The class has also some useful helper methods as **space_saving**, **size**, and **decompress()** to revert back to original.

Another example with numeric data.

```python
from random import sample, choices

numbers = choices(sample(range(0, 5), 5), k = 20)
comp_num = lzhw.LZHW(numbers)

print(getsizeof(numbers) > comp_num.size())
# True

print(numbers == list(map(int, comp_num.decompress()))) ## make it int again
# True

print(comp_num.space_saving())
# space saving from original to compressed is 73%
```

Let's look at how the compressed object is stored and how it looks like when printed:
LZHW class has an attribute called **compressed** which is a tuple of integers representing the encoded triplets.

```python
print(comp_num.compressed) # how the compressed is saved (as tuple of 3 integers)
# (8198555, 620206, 3059308)
```

We can also write the compressed data to files using **save_to_file** method, 
and read it back and decompress it using **decompress_from_file** function.

```python
status = ["Good", "Bad", "Bad", "Bad", "Good", "Good", "Average", "Average", "Good",
          "Average", "Average", "Bad", "Average", "Good", "Bad", "Bad", "Good"]
comp_status = lzhw.LZHW(status)
comp_status.save_to_file("status.txt")
decomp_status = lzhw.decompress_from_file("status.txt")
print(status == decomp_status)
# True
```

## Compressing DataFrames

lzhw doesn't work only on lists, it also compress pandas dataframes and save it into compressed files to decompress them later.

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 1, 2, 2, 1, 3, 4, 4],
                   "b": ["A", "A", "B", "B", "A", "C", "D", "D"]})
comp_df = lzhw.CompressedDF(df)
# 100%|██████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 2003.97it/s]
```

Let's check space saved by compression
```python
comp_space = 0
for i in range(len(comp_df.compressed)):
	comp_space += comp_df.compressed[i].size()

print(comp_space, getsizeof(df))
# 144 712

## Test information loss
print(comp_df.compressed[0].decompress() == list(map(str, df.a)))
# True
```

#### Saving and Loading Compressed DataFrames

With lzhw we can save a data frame into a compressed file and then read it again 
using **save_to_file** method and **decompress_df_from_file** function.

```python
## Save to file
comp_df.save_to_file("comp_df.txt")

## Load the file
original = lzhw.decompress_df_from_file("comp_df.txt")
# 100%|██████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 2004.93it/s]

print(original)
#   a  b
#0  1  A
#1  1  A
#2  2  B
#3  2  B
#4  1  A
#5  3  C
#6  4  D
#7  4  D
```

#### Compressing Bigger DataFrames

Let's try to compress a real-world dataframe **german_credit.xlsx** file from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)) [1].

Original txt file is **219 KB** on desk.

```python
gc_original = pd.read_excel("examples/german_credit.xlsx")
comp_gc = lzhw.CompressedDF(gc_original)
# 100%|█████████████████████████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 257.95it/s]

## Compare sizes in Python:
comp_space = 0
for i in range(len(comp_gc.compressed)):
	comp_space += comp_gc.compressed[i].size()

print(comp_space, getsizeof(gc_original))
# 4504 548852

print(comp_gc.compressed[0].decompress() == list(map(str, gc_original.iloc[:, 0])))
# True
```

**Huge space saving, 99%, with no information loss!**

Let's now write the compressed dataframe into a file and compare the sizes of the files.

```python
comp_gc.save_to_file("gc_compressed.txt")
``` 

Checking the size of the compressed file, it is **44 KB**. Meaning that in total we saved around **79%**.
Future versions will be optimized to save more space.

Let's now check when we reload the file, will we lose any information or not.

```python
## Load the file
gc_original2 = lzhw.decompress_df_from_file("gc_compressed.txt")
# 100%|█████████████████████████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 259.46it/s]

print(list(gc_original2.iloc[:, 13]) == list(map(str, gc_original.iloc[:, 13])))
# True

print(gc_original.shape == gc_original2.shape)
# True
```

**Perfect! There is no information loss at all.**

## (De)Compressing specific columns or rows from a dataframe

With **lzhw** you can choose what columns you are interested in compressing from a data frame.
**CompressedDF** class has an argument **selected_cols**.
```python
gc_original = pd.read_excel("examples/german_credit.xlsx")
comp_gc = lzhw.CompressedDF(gc_original, selected_cols = [0, 3, 4, 7])
# 100%|███████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 401.11it/s]
``` 
Also when you have a compressed file that you want to decompress, you don't have to decompress it all, you can choose only specific columns and/or rows to decompress.
By this you can deal with large compressed files and do operations **column by column** quickly and **avoid memory errors**
**decompress_df_from_file** function has the same argument **selected_cols**.
```python
gc_original2 = lzhw.decompress_df_from_file("gc_compressed.txt", selected_cols = [0, 4])
# 100%|████████████████████████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 3348.53it/s]

gc_original2.head()
#	Duration	Age
#0	       6	67
#1	      48	22
#2	      12	49
#3	      42	45
#4	      24	53
```
Let's compare this subset with the original df.
```python
gc_original.iloc[:, [0, 4]].head()
#	Duration	Age
#0	       6	67
#1	      48	22
#2	      12	49
#3	      42	45
#4	      24	53
```
Perfect!

*selected_cols* has "all" as its default value.

**decompress_df_from_file** has another argument which is **n_rows** to specify the number of rows we would like to decompress only.

The argument's default value is **0** to decompress all data frame, if specified it will decompress from start until desired number of rows.
```python
gc_original_subset = lzhw.decompress_df_from_file("gc_compressed.txt", n_rows = 6)
# 100%|████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 914.21it/s]

print(gc_original_subset.shape)
# (6, 62)
```

This can be very helpful when reading very big data in chunks of rows and columns to avoid **MemoryError** and to apply **operations** and **online algorithms** **faster**.

```python
gc_original_subset_smaller = lzhw.decompress_df_from_file("gc_compressed.txt", 
                                                  selected_cols = [1, 4, 8, 9], 
                                                  n_rows = 6)
# 100%|████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 3267.86it/s]

print(gc_original_subset_smaller.shape)
# (6, 4)

print(gc_original_subset_smaller)
#   Amount Age ForeignWorker Class
# 0   1169  67             1  Good
# 1   5951  22             1   Bad
# 2   2096  49             1  Good
# 3   7882  45             1  Good
# 4   4870  53             1   Bad
# 5   9055  35             1  Good
```

## Using the lzhw Command Line Interface

In **lzhw_cli** folder, there is a python script that can work on command line to compress and decompress files.

Here is the file:
```bash
$python lzhw_cli.py

usage: lzhw_cli.py [-h] [-d] -f INPUT -o OUTPUT [-c COLUMNS [COLUMNS ...]]
                   [-nh]
lzhw_cli.py: error: the following arguments are required: -f/--input, -o/--output
```

Getting help to see what it does and its arguments:
```bash
$python lzhw_cli.py -h

usage: lzhw_cli.py [-h] [-d] -f INPUT -o OUTPUT [-c COLUMNS [COLUMNS ...]]
                   [-nh]

Data Frame Compressor

optional arguments:
  -h, --help            show this help message and exit
  -d, --decompress      decompress input into output
  -f INPUT, --input INPUT
                        input file to be (de)compressed
  -o OUTPUT, --output OUTPUT
                        output where to save result
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        select specific columns by names or indices (1-based)
  -r ROWS, --rows ROWS  select specific rows to decompress (1-based)
  -nh, --no-header      skip header / data has no header
```

How to compress:
```bash
$python lzhw_cli.py -f "file_to_compress" -o "output"

compressed successfully
```

How to decompress:
```bash
$python lzhw_cli.py -d -f "file_to_decompress" -o "output"

decompressed successfully
```
## Helper Functions

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

##### Reference
###### 		[1] Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

