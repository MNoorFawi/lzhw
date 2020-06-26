# Compressing DataFrames (in Parallel)

#### From DataFrame to CompressedDF
lzhw doesn't work only on lists, it also compress pandas dataframes and save it into compressed files to decompress them later.

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 1, 2, 2, 1, 3, 4, 4],
                   "b": ["A", "A", "B", "B", "A", "C", "D", "D"]})
comp_df = lzhw.CompressedDF(df)
# 100%|██████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 2003.97it/s]
```

Let's check space saved by compression
```python
comp_space = 0
for i in range(len(comp_df.compressed)):
	comp_space += comp_df.compressed[i].size()

print(comp_space, getsizeof(df))
# 144 712

## Test information loss
print(all(comp_df.compressed[0].decompress() == list(map(str, df.a))))
# True
```

#### Saving and Loading Compressed DataFrames

With lzhw we can save a data frame into a compressed file and then read it again 
using **save_to_file** method and **decompress_df_from_file** function.

**Let's try to decompress in parallel**

```python
## Save to file
comp_df.save_to_file("comp_df.txt")

## Load the file
original = lzhw.decompress_df_from_file("comp_df.txt", parallel = True)
# 100%|█████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 2004.93it/s]

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
gc_original = pd.read_excel("examples/german_credit.xlsx", 
                            parallel = True, n_jobs = -3) # default value all CPUs but 2
comp_gc = lzhw.CompressedDF(gc_original)
# 100%|█████████████████████████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 257.95it/s]

## Compare sizes in Python:
comp_space = 0
for i in range(len(comp_gc.compressed)):
	comp_space += comp_gc.compressed[i].size()

print(comp_space, getsizeof(gc_original))
# 4488 548852

print(all(comp_gc.compressed[0].decompress() == list(map(str, gc_original.iloc[:, 0]))))
# True
```

**Huge space saving, 99%, with no information loss!**

Let's now write the compressed dataframe into a file and compare the sizes of the files.

```python
comp_gc.save_to_file("gc_compressed.txt")
``` 

Checking the size of the compressed file, it is **38 KB**. Meaning that in total we saved around **82%**.
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

##### Reference
 		[1] Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
