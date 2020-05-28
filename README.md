# lzhw

[![](https://img.shields.io/badge/docs-latest-blue.svg)](https://mnoorfawi.github.io/lzhw/) 
[![Build Status](https://travis-ci.com/MNoorFawi/lzhw.svg?branch=master)](https://travis-ci.com/MNoorFawi/lzhw)

**Compression** library to compress big lists and/or pandas dataframes using an **optimized algorithm (lzhw)** developed from Lempel-Ziv, Huffman and LZ-Welch techniques.

## Quick Start

```bash
pip install lzhw
```

```python
import lzhw

sample_data = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny",
               "Rain", "Sunny", "Overcast", "Overcast", "Rain", "Rain", "Rain", "Sunny", "Sunny", 
			   "Overcaste"]

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

Checking the size of the compressed file, it is **134 KB**. Meaning that in total we saved around **39%**.
Future versions will be optimized to save more space.

Let's now check when we reload the file, will we lose any information or not.

```python
## Load the file
gc_original2 = lzhw.decompress_df_from_file("gc_compressed.txt")
print(list(gc_original2.iloc[:, 13]) == list(map(str, gc_original.iloc[:, 13])))
# True

print(gc_original.shape == gc_original2.shape)
# True
```

Perfect! There is no information loss at all.