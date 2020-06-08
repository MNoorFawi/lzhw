# (De)Compressing specific columns from a dataframe

With **lzhw** you can choose what columns you are interested in compressing from a data frame.
**CompressedDF** class has an argument **selected_cols**.
```python
import lzhw
import pandas as pd
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

We can also select columns by names:
```python
gc_subset = lzhw.decompress_df_from_file("gc_compressed.txt", 
                                         selected_cols=["Age", "Duration"])
# 100%|████████████████████████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 6220.92it/s]

print(gc_subset.head())
# Duration	Age
#0	 6	67
#1	48	22
#2	12	49
#3	42	45
#4	24	53
```

*selected_cols* has "all" as its default value.
