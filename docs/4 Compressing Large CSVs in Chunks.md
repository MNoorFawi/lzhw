# Compressing Large CSVs in Chunks

#### Compressed Chunks

With **lzhw** we can also compressed a large csv file without needing to read it all in memory using **CompressedFromCSV** method.

It uses **pandas chunksize** argument to read the file in chunks and compress each chunk and return a **dictionary of compressed chunks.**

We can also specify **selected_cols** argument to get only specific columns from a file. And **parallel** argument in case we want to compress each chunk in parallel.

Default chunk size is 1 million. So it is preferably to be used with very large files.

Let's assume that **german Credit**[1] data is a big one just for illustration.

Because the data is in excel and CompressedFromCSV only works with csv we will change the file into csv first.
```python
import pandas as pd
gc = pd.read_excel("examples/german_credit.xlsx")
gc.to_csv("german_credit.csv", index = False)

chunks = gc.shape[0] / 4 ## to have 4 chunks
compressed_chunks = lzhw.CompressedFromCSV("german_credit.csv", chunksize = chunks)
# Compressing Chunk 0 ...
# 100%|█████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 1478.93it/s]
# Compressing Chunk 1 ...
# 100%|█████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 1515.10it/s]
# Compressing Chunk 2 ...
# 100%|█████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 1678.66it/s]
# Compressing Chunk 3 ...
# 100%|█████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 1635.98it/s]
# File was compressed in 4 chunk(s)
```

#### Dictionary of Compressed Chunks
We now have a dictionary of four compressed chunks.
Let's look at it.
```python
## How many chunks
print(compressed_chunks.chunk_ind)
# 4

## Chunk id is the key to get the compressed chunk of data frame
print(compressed_chunks.all_comp.keys())
# dict_keys([0, 1, 2, 3])

## the dicionary
print(compressed_chunks.all_comp)
# {0: <lzhw.lzhw_df.CompressedDF at 0x23e29ae75c8>,
#  1: <lzhw.lzhw_df.CompressedDF at 0x23e2c467f08>,
#  2: <lzhw.lzhw_df.CompressedDF at 0x23e29bb7408>,
#  3: <lzhw.lzhw_df.CompressedDF at 0x23e29cfb4c8>}
```

As we can see, **4 chunks of 4 CompressedDF class**, we can now treat them separately.

```python
## Let's decompress column 0 from chunk 0 and compare it with original 0 column in data
gc_chunk00 = compressed_chunks.all_comp[0].compressed[0].decompress()
print(all(gc_chunk00 == gc.iloc[:int(chunks), 0])) # because each chunk has a slice of the original dataframe
# True
```
#### Saving and Reading Compressed Chunks
Finally, we can save the dictionary to desk using **save_to_file** method and read it using **decompress_df_from_file** method.
```python
compressed_chunks.save_to_file("compressed_chunks.txt", chunks = "all")
```
**We can specify the chunks we want to save to file. Default is "all".**

**Also while decompressing we can only get specific chunks**
```python
decomp_chunks = lzhw.decompress_df_from_file("compressed_chunks.txt",
                                             selected_chunks = [0, 3])
# 100%|█████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 3265.44it/s]
# 100%|█████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 3113.33it/s]
```
Each chunk contains a decompressed data frame inside it. Let's check that only two chunks were decompressed:
```python
print(decomp_chunks.keys())
# dict_keys([0, 3])

total_rows = 0
for k in decomp_chunks.keys():
    total_rows += decomp_chunks[k].shape[0]
print(total_rows)
# 500
```
Seems perfect! Data was compressed in 4 chunks 250 rows each, as all data is of 1000 rows.

Let's look at the contained data frames
```python
print(decomp_chunks[0].iloc[:4, :3])
# 	Duration	Amount	InstallmentRatePercentage
# 0	       6	  1169	                        4
# 1	      48	  5951	                        2
# 2	      12	  2096	                        2
# 3	      42	  7882	                        2
```

##### Reference
 		[1] Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
