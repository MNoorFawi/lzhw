# Using the lzhw Command Line tool

![](./img/lzhw_logo.jpg)

Using **lzhw_cli** script and [pyinstaller](https://www.pyinstaller.org/), We generate a command line tool that does compression and decompression using **lzhw** functionalities without any prior installations or dependencies.

#### LZHW Compression Tool

**The tool can be downloaded from the releases tab**

**The tool allows to compress and decompress files from and to any form, csv, excel etc without any dependencies or installations.**

**The tool can work in parallel and most of its code is written in Cython, so it is pretty fast**. Next page in the documentation there is a comparison in performance with other tools.

The tool now works perfectly on Windows for now, both Linux and Mac versions are being developed soon.

#### Getting Started

Here is the file and its help argument to see how it works and its arguments:
```bash
lzhw -h
```
Output
```bash
usage: lzhw [-h] [-d] -f INPUT -o OUTPUT [-c COLUMNS [COLUMNS ...]] [-r ROWS]
            [-nh] [-p] [-j JOBS]

LZHW is a tabular data compression tool. It is used to compress excel, csv and
any flat file. Version: 0.0.10

optional arguments:
  -h, --help            show this help message and exit
  -d, --decompress      decompress input into output
  -f INPUT, --input INPUT
                        input file to be (de)compressed
  -o OUTPUT, --output OUTPUT
                        output where to save result
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        select specific columns by names or indices (1-based)
                        to compress or decompress
  -r ROWS, --rows ROWS  select specific rows to decompress (1-based)
  -nh, --no-header      skip header / data to be compressed has no header
  -p, --parallel        compress or decompress in parallel
  -j JOBS, --jobs JOBS  Number of CPUs to use if parallel (default all but 2)
```
As we can see, the tool takes an input file **"-f"**, and output **"-o"** where it should put the result whether it is compression or decompression based on the optional **"-d"** argument which selects decompression.

The tool as well takes a **"-c"** argument which is the Columns in case we want only to compress or decompress specific columns from the input file instead of dealing with all the columns unnecessarily.
This argument accepts names and indices separated by coma.

The **"-nh"**, --no-header, argument to specify if the data has no header.

The **"-r"**, --rows, argument is to specify number of rows to decompress, in case we don't need to decompress all rows.

The **"-p"**, --parallel, argument is to make compression and decompression goes in parallel to speed it up. And specifying the **"-j"**, --jobs, argument to determine the number of the CPUs to be used, in default it is all CPUs minus 2.

#### Compress
How to compress:

The tool can be used through command line. 
For those who are new to command line, the easiest way to start it is to put the **lzhw.exe** tool in the same folder with the sheet you want to compress.
Then go to the folder's directory at the top where you see the directory path and one click then type **cmd**, black command line will open to you where you can type the examples below.
  
*Using german_credit data from UCI Machine Learning Repository [1]* 
```bash
lzhw -f "german_credit.xlsx" -o "gc_comp.txt"
```
```bash
Reading files, Can take 1 minute or something ...
Running CScript.exe to convert xls file to csv for better performance

Microsoft (R) Windows Script Host Version 5.812
Copyright (C) Microsoft Corporation. All rights reserved.

100%|██████████████████████████████████████████████████████████████████| 62/62 [00:02<00:00, 21.92it/s]
Finalizing Compression ...
Creating gc_comp.txt file ...
time taken:  0.06792410214742024  minutes
Compressed Successfully
```

**In parallel**:
```bash
lzhw -f "german_credit.xlsx" -o "gc_comp.txt" -p
```
```bash
Reading files, Can take 1 minute or something ...
Running CScript.exe to convert xls file to csv for better performance

Microsoft (R) Windows Script Host Version 5.812
Copyright (C) Microsoft Corporation. All rights reserved.

100%|███████████████████████████████████████████████████████████████████| 62/62 [00:00<00:00, 74.28it/s]
Finalizing Compression ...
Creating gc_comp.txt file ...
time taken:  0.030775876839955647  minutes
Compressed Successfully
```

Now, let's say we are interested only in compressing the Age, Duration and Amount columns
```bash
lzhw -f "german_credit.xlsx" -o "gc_subset.txt" -c Age,Duration,Amount
```
```bash
Reading files, Can take 1 minute or something ...
Running CScript.exe to convert xls file to csv for better performance

Microsoft (R) Windows Script Host Version 5.812
Copyright (C) Microsoft Corporation. All rights reserved.

100%|███████████████████████████████████████████████████| 3/3 [00:00<00:00, 249.99it/s]
Finalizing Compression ...
Creating gc_subset.txt file ...
time taken:  0.01437713384628296  minutes
Compressed Successfully
```
#### Decompress
Now it's time to decompress:

**If your original excel file was big and of many rows and columns, it's better and faster to decompress it into a csv file instead of excel directly and then save the file as excel if excel type is necessary. This is because python is not that fast in writing data to excel as well as the tool sometimes has "Corrupted Files" issues with excel.**

Decompressing in parallel using 2 CPUs.
```bash
lzhw -d -f "gc_comp.txt" -o "gc_decompressed.csv" -p -j 2
```
```bash
100%|████████████████████████████████████████████████████| 62/62 [00:00<00:00, 99.00it/s]
Finalizing Decompression ...
Creating gc_decompressed.csv file ...
time taken:  0.014344350496927897  minutes
Decompressed Successfully
```
Look at how the **-d** argument is used.

Let's now check that it was decompressed really successfully:
```bash
head -n 4 gc_decompressed.csv

Duration,Amount,InstallmentRatePercentage,ResidenceDuration,Age,NumberExistingCredits,NumberPeopleMaintenance,Telephone,ForeignWorker,Class,CheckingAccountStatus.lt.0,CheckingAccountStatus.0.to.200,CheckingAccountStatus.gt.200,CheckingAccountStatus.none,CreditHistory.NoCredit.AllPaid,CreditHistory.ThisBank.AllPaid,CreditHistory.PaidDuly,CreditHistory.Delay,CreditHistory.Critical,Purpose.NewCar,Purpose.UsedCar,Purpose.Furniture.Equipment,Purpose.Radio.Television,Purpose.DomesticAppliance,Purpose.Repairs,Purpose.Education,Purpose.Vacation,Purpose.Retraining,Purpose.Business,Purpose.Other,SavingsAccountBonds.lt.100,SavingsAccountBonds.100.to.500,SavingsAccountBonds.500.to.1000,SavingsAccountBonds.gt.1000,SavingsAccountBonds.Unknown,EmploymentDuration.lt.1,EmploymentDuration.1.to.4,EmploymentDuration.4.to.7,EmploymentDuration.gt.7,EmploymentDuration.Unemployed,Personal.Male.Divorced.Seperated,Personal.Female.NotSingle,Personal.Male.Single,Personal.Male.Married.Widowed,Personal.Female.Single,OtherDebtorsGuarantors.None,OtherDebtorsGuarantors.CoApplicant,OtherDebtorsGuarantors.Guarantor,Property.RealEstate,Property.Insurance,Property.CarOther,Property.Unknown,OtherInstallmentPlans.Bank,OtherInstallmentPlans.Stores,OtherInstallmentPlans.None,Housing.Rent,Housing.Own,Housing.ForFree,Job.UnemployedUnskilled,Job.UnskilledResident,Job.SkilledEmployee,Job.Management.SelfEmp.HighlyQualified
6,1169,4,4,67,2,1,0,1,Good,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0
48,5951,2,2,22,1,1,1,1,Bad,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0
12,2096,2,3,49,1,2,1,1,Good,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,0
```
It looks awful in the command line :D but it's decompressed.

Now let's say that we only interested in decompressing the first two columns that we don't remember how they were spelled.
```bash
lzhw -d -f "gc_comp.txt" -o "gc_subset_de.csv" -c 1,2 
```
```bash
100%|███████████████████████████████████████████████████| 2/2 [00:00<00:00,  8.05it/s]
Finalizing Decompression ...
Creating gc_subset_de.csv file ...
time taken:  0.00028291543324788414  minutes
Decompressed Successfully
```
Now let's have a look at the decompressed file:
```bash
head gc_subset_de.csv

Duration,Amount
6,1169
48,5951
12,2096
42,7882
24,4870
36,9055
24,2835
36,6948
12,3059
```

We can also use the **-r** argument to decompress specific rows from the data frame.

```bash
lzhw -d -f "gc_comp.txt" -o "gc_subset_de.csv" -r 4

100%|████████████████████████████████████████████████████| 62/62 [00:00<00:00, 369.69it/s]
Finalizing Decompression ...
Creating gc_subset_de.csv file ...
time taken:  0.007962568600972494  minutes
Decompressed Successfully
```

Here we only decompressed the first 4 rows, 1-based, including the header.

Let's look how the data looks like:

```bash
cat "gc_subset_de.csv"

Duration,Amount,InstallmentRatePercentage,ResidenceDuration,Age,NumberExistingCredits,NumberPeopleMaintenance,Telephone,ForeignWorker,Class,CheckingAccountStatus.lt.0,CheckingAccountStatus.0.to.200,CheckingAccountStatus.gt.200,CheckingAccountStatus.none,CreditHistory.NoCredit.AllPaid,CreditHistory.ThisBank.AllPaid,CreditHistory.PaidDuly,CreditHistory.Delay,CreditHistory.Critical,Purpose.NewCar,Purpose.UsedCar,Purpose.Furniture.Equipment,Purpose.Radio.Television,Purpose.DomesticAppliance,Purpose.Repairs,Purpose.Education,Purpose.Vacation,Purpose.Retraining,Purpose.Business,Purpose.Other,SavingsAccountBonds.lt.100,SavingsAccountBonds.100.to.500,SavingsAccountBonds.500.to.1000,SavingsAccountBonds.gt.1000,SavingsAccountBonds.Unknown,EmploymentDuration.lt.1,EmploymentDuration.1.to.4,EmploymentDuration.4.to.7,EmploymentDuration.gt.7,EmploymentDuration.Unemployed,Personal.Male.Divorced.Seperated,Personal.Female.NotSingle,Personal.Male.Single,Personal.Male.Married.Widowed,Personal.Female.Single,OtherDebtorsGuarantors.None,OtherDebtorsGuarantors.CoApplicant,OtherDebtorsGuarantors.Guarantor,Property.RealEstate,Property.Insurance,Property.CarOther,Property.Unknown,OtherInstallmentPlans.Bank,OtherInstallmentPlans.Stores,OtherInstallmentPlans.None,Housing.Rent,Housing.Own,Housing.ForFree,Job.UnemployedUnskilled,Job.UnskilledResident,Job.SkilledEmployee,Job.Management.SelfEmp.HighlyQualified
6,1169,4,4,67,2,1,0,1,Good,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0
48,5951,2,2,22,1,1,1,1,Bad,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0
12,2096,2,3,49,1,2,1,1,Good,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,0
42,7882,2,4,45,1,2,1,1,Good,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,1,0,0,1,0
```

All data is now 5 rows only including the header.

#### Notes on the Tool

**1- compression is much faster than decompression, it is good to compress sequentially and decompress in parallel.**

**2- This error message can appear while compressing or decompressing in parallel**
```bash
lzhw.exe [-h] [-d] -f INPUT -o OUTPUT [-c COLUMNS [COLUMNS ...]]
                [-r ROWS] [-nh]
lzhw.exe: error: the following arguments are required: -f/--input, -o/--output
```
**It is totally fine, just press Enter and proceed or leave it until it tells you "Compressed Successsfully" or "Decompressed Successfully"**.

The error is due to some parallelization library bug that has nothing to do with the tool so it is ok.

**3- The progress bar of columns compression, it doesn't mean that the tool has finished because it needs still to write the answers. So you need to wait until "Compressed Successfully" or "Decompressed Successfully" message appears.**

**4- The tool takes a couple of seconds from 8 to 15 seconds to start working and compressing at the first time and then it runs faster and faster the more you use it.** 

#### Developing the Tool Using PyInstaller
In case you have python installed and you want to develop the tool yourself. Here is how to do it:

First let's make sure we create a new environment, because pyinstaller wraps up all the libraries installed so the generated file can be large.
So we only need to wrap the required libraries.

Then we install pyinstaller and required libraries which are:
```bash
pip install setuptools
pip install lzhw
pip install xlsxwriter ## because sometimes it is missing
pip install openpyxl  ## because sometimes it is missing
pip install pyinstaller
```

Then, because sometimes the generated file gives a **No Module pkg_resource** error, we can navigate to the hooks folder in pyinstaller and open **hook-pkg_resources.py** file and write **hiddenimports.append('pkg_resources.py2_warn')** in the penultimate line.

Then we are ready to go and in the command line we need to type:
```bash
pyinstaller --noconfirm --onefile --console --icon "lzhw_logo.ico" "lzhw_cli.py"
```
And the tool will be generated in *dist* folder.

Sometimes the tool gives memmapping warning while running, so to suppress those warnings, in the *spec* file we can write **[('W ignore', None, 'OPTION')]** inside **exe = EXE()**. and then **pyinstaller lzhw_cli.spec**.

##### Reference
 		[1] Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
