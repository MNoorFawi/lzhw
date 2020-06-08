# Quick Start

Here is a quick walkthrough to get started with the library.

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
# (506460, 128794, 105942)

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
# (291314557, 351007, 116989796)
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