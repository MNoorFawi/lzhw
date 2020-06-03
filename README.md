# lzhw

[![](https://img.shields.io/badge/docs-latest-blue.svg)](https://mnoorfawi.github.io/lzhw/) 
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
**lzhw** uses **lz78** to discover repeated sequences in the stream and construct a dictionary, but instead of returning their codes from the dictionary, it glues the sequence together in one cell.
Then we will have a shorter list with repeated sequences glued together, where **Huffman Coding** can come to the game encoding them.

The function that performs lempel-ziv and returning a shorter list without the codes I named it **lz20** :D.
```python
import lzhw
lz20_ex = lzhw.lz20(example)
print(lz20_ex)
# ['to', 'be', 'or', 'not', 'to', 'be', 'or', 'to', 'be', 'or', 
#  'not', 'to', 'be or', 'not', 'to be', 'or', 'to be or', 'not']
```
Now huffman coding will give us:
```python
from collections import Counter
huff20 = lzhw.huffman_coding(Counter(lz20_ex))
print(huff20)
# {'to': '10', 'be': '110', 'or': '01', 'not': '00', 
#  'be or': '11110', 'to be': '11111', 'to be or': '1110'}
```
This will give us:
```python
print("".join([huff20.get(i) for i in lz20_ex]))
# 10110010010110011011001001011110001111101111000
```
Which has a length of 47 bits.

Then it uses **lempel-ziv-welch (lzw)** to compress the keys of the dictionaries so that no need to store them as strings, i.e. extra space saving.
```python
from sys import getsizeof
some_key = "to be or"
print(getsizeof(some_key))
# 57

lzw_key = lzhw.lzw_compress(some_key)
print(lzw_key)
# 5794278370027331706482

print(getsizeof(lzw_key))
# 36
```
Let's see if we store the keys of the dictionary as string how much size they will have in comparison of the integer type.
```python
keys = list(huff20.keys())
print(getsizeof(keys))
# 144

comp_keys = [lzhw.lzw_compress(k) for k in keys]
print(getsizeof(comp_keys))
# 128
```

All of the steps can be done at once using **LZHW** class as follows and as shown in the Quick Start section:
```python
lzhw_comp = lzhw.LZHW(example)
print(lzhw_comp)
# 110110010010110011011001001011110001111101111000 
# the first 1 is a to save the preceeding 0s as compressed data is stored as an integer
print(lzhw_comp.compressed)
# 238786645532536

print(lzhw_comp.sequences) # dictionary's keys and values are stored as integers as well
# {6: 321647, 14: 312421, 5: 319090, 4: 163110516, 62: 41932445245042,
#  63: 43170737996901, 30: 5794278370027331706482}
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
print(compressed)
# 1111101101010011111101101010011100000010

## its size
print(compressed.size())
# 32

## size of original
from sys import getsizeof
print(getsizeof(sample_data))
# 216

print(compressed.space_saving())
# space saving from original to compressed is 85%

## Let's decompress and check whether there is any information loss
decomp = compressed.decompress()
print(decomp == sample_data)
# True
```

As we saw, the LZHW class has saved 85% of the space used to store the original list without any loss.
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
# space saving from original to compressed is 88%
```

Let's look at how the compressed object is stored and how it looks like when printed:
LZHW class has an attribute called **compressed** which is the integer of the encoded bitstring

```python
print(comp_num.compressed) # how the compressed is saved (as integer of the bit string)
# 103596881534874

print(comp_num)
# 10111100011100010000111010100101101111110011010
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
# 56 712

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

Let's try to compress a real-world dataframe **german_credit.xlsx** file.
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
# 12932 548852

print(comp_gc.compressed[0].decompress() == list(map(str, gc_original.iloc[:, 0])))
# True
```

**Huge space saving, 97%, with no information loss!**

Let's now write the compressed dataframe into a file and compare the sizes of the files.

```python
comp_gc.save_to_file("gc_compressed.txt")
``` 

Checking the size of the compressed file, it is **87 KB**. Meaning that in total we saved around **60%**.
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

Perfect! There is no information loss at all.

## (De)Compressing specific columns from a dataframe

With **lzhw** you can choose what columns you are interested in compressing from a data frame.
**CompressedDF** class has an argument **selected_cols**.
```python
gc_original = pd.read_excel("examples/german_credit.xlsx")
comp_gc = lzhw.CompressedDF(gc_original, selected_cols = [0, 3, 4, 7])
# 100%|███████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 401.11it/s]
``` 
Also when you have a compressed file that you want to decompress, you don't have to decompress it all, you can choose only specific columns to decompress.
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

## Using the lzhw Command Line Interface

In **lzhw_cli** folder, there is a python script that can work on command line to compress and decompress files.

Here is the file:
```bash
$python lzhw_cli.py

usage: lzhw_cli.py [-h] [-d] -f INPUT -o OUTPUT
lzhw_cli.py: error: the following arguments are required: -f/--input, -o/--output
```

Getting help to see what it does and its arguments:
```bash
$python lzhw_cli.py -h

usage: lzhw_cli.py [-h] [-d] -f INPUT -o OUTPUT

Data Frame Compressor

optional arguments:
  -h, --help            show this help message and exit
  -d, --decompress      decompress input into output
  -f INPUT, --input INPUT
                        input file to be (de)compressed
  -o OUTPUT, --output OUTPUT
                        output where to save result
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

**lz78** which performs the famous **lempel-ziv78** algorithm:
```python
import random
random.seed(1311)
example = random.choices(["A", "B", "C"], k = 20)
print(example)
#['A', 'A', 'C', 'C', 'A', 'A', 'C', 'C', 'C', 'B', 'B', 'A', 'B', 'B', 'C', 'C', 'B', 'C', 'C', 'B']

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

They perform **lempel-ziv-welch** compressing and decompressing
```python
print(lzhw.lzw_compress("Hello World"))
# 723201696971929295664359987300

print(lzhw.lzw_decompress(lzhw.lzw_compress("Hello World")))
# Hello World
```
