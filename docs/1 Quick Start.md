# Quick Start

Here is a quick walkthrough to get started with the library.
#### Installation
```bash
pip install lzhw
```
#### LZHW Class
```python
import lzhw

sample_data = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", 
               "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain", 
               "Rain", "Rain", "Sunny", "Sunny", "Overcaste"]

compressed = lzhw.LZHW(sample_data)
## let's see how the compressed object looks like:
print(compressed.compressed)
# (524288, 524288, 81592676324)

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
print(all(decomp == sample_data))
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
#### A Long List to 3 Numbers
Let's look at how the compressed object is stored and how it looks like when printed:
LZHW class has an attribute called **compressed** which is a tuple of integers representing the encoded triplets.

```python
print(comp_num.compressed) # how the compressed is saved (as tuple of 3 integers)
# (1048576, 1048576, 43175655208435)
```
#### Adjusting Sliding Window
LZHW class has **sliding_window** argument which we can adjust in case we want more compression. 

The sliding window is where the algorithm looks back for previous sequences matching the current location in the input stream. 

The default value of the argument is 265 meaning that the algorithm will look for matches in the previous 265 values from the current location.

We can make this number bigger to allow the algorithm to look for matches in a wider window that can potentially lead to more compression. The algorithm then will behave a little bit slower, you may even not notice it, because **lzhw uses hash table, python dictionaries, to look up the matches, i.e. it doesn't loop over the window elements.**

```python
from time import time
from sys import getsizeof
sample_data = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", 
               "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain", 
               "Rain", "Rain", "Sunny", "Sunny", "Overcaste"] * 10000
print("Original size:", getsizeof(sample_data))
# Original size: 1520064

start = time()
lzhw265 = lzhw.LZHW(sample_data, sliding_window = 265)
print("sliding window 265 compression time:", time() - start)
# sliding window 265 compression time: 0.5186636447906494

print("sliding window 265 size:", lzhw265.size())
# sliding window 265 size: 72

start = time()
lzhw1024 = lzhw.LZHW(sample_data, sliding_window = 1024)
print("sliding window 1024 compression time:", time() - start)
# sliding window 1024 compression time: 0.5305755138397217

print("sliding window 1024 size:", lzhw1024.size())
# sliding window 1024 size: 72
```
Time difference is almost not noticeable, and size is the same because the output is a tuple of 3 integers and the data itself is repeated 10k times so changing the sliding window will not help. Here it is for illustration only but you will notice the difference with real data when you save it into desk.
#### Writing to & Reading from Files
We can also write the compressed data to files using **save_to_file** method, 
and read it back and decompress it using **decompress_from_file** function.

```python
status = ["Good", "Bad", "Bad", "Bad", "Good", "Good", "Average", "Average", "Good",
          "Average", "Average", "Bad", "Average", "Good", "Bad", "Bad", "Good"]
comp_status = lzhw.LZHW(status)
comp_status.save_to_file("status.txt")
decomp_status = lzhw.decompress_from_file("status.txt")
print(all(status == decomp_status))
# True
```
