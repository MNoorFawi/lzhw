# Using the lzhw Command Line tool

In **lzhw_cli** folder, there is a python script that can work on command line tool to compress and decompress files without having to open it in python.
#### LZHW Compression Tool
**Also a downloadable exe tool is available in this [link](https://drive.google.com/file/d/1CBu7Adb5CHZUwhANa_i8Es0-8jSWAmiC/view?usp=sharing).**
**The tool allows to compress and decompress files from and to any form, csv,xlsx etc without any dependencies or installations.**

The tool now works perfectly on Windows and Mac version is being developed.

Here is the file and its help argument to see how it works and its arguments:
```bash
lzhw -h
```
Output
```bash
usage: lzhw_cli.py [-h] [-d] -f INPUT -o OUTPUT [-c COLUMNS [COLUMNS ...]]
                   [-r ROWS] [-nh]

LZHW is a tabular data compression tool. It is used to compress excel, csv and
any flat file. Version: 0.0.8

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
```
As we can see, the tool takes an input file **"-f"**, and output **"-o"** where it should put the result whether it is compression or decompression based on the optional **"-d"** argument which selects decompression.

The tool as well takes a **"-c"** argument which is the Columns in case we want only to compress or decompress specific columns from the input file instead of dealing with all the columns unnecessarily.
This argument accepts names and indices seperated by coma.

The **"-nh"**, --no-header, argument to specify if the data has no header.

The **"-r"**, --rows, argument is to specify number of rows to decompress, in case we don't need to decompress all rows.

#### Compress
How to compress:

The tool can be used through command line. 
For those who are new to command line, the easiest way to start it is to put the **lzhw.exe** tool in the same folder with the sheet you want to compress.
Then go to the folder's directory at the top where you see the directory path and one click then type **cmd**, black command line will open to you where you can type the examples below.
  

```bash
lzhw -f "german_credit.xlsx" -o "gc_comp.txt"
```
```bash
Reading files, Can take 1 minute or something ...
Running CScript.exe to convert xls file to csv for better performance

Microsoft (R) Windows Script Host Version 5.812
Copyright (C) Microsoft Corporation. All rights reserved.

100%|███████████████████████████████████████████████████| 62/62 [00:00<00:00, 647.30it/s]
Creating gc_comp.txt file ...
Compressed Successfully
```
Let's say we are interested only in compressing the Age, Duration and Amount columns
```bash
lzhw -f "german_credit.xlsx" -o "gc_subset.txt" -c Age,Duration,Amount
```
```bash
Reading files, Can take 1 minute or something ...
Running CScript.exe to convert xls file to csv for better performance

Microsoft (R) Windows Script Host Version 5.812
Copyright (C) Microsoft Corporation. All rights reserved.

100%|███████████████████████████████████████████████████| 3/3 [00:00<00:00, 249.99it/s]
Creating gc_subset.txt file ...
Compressed Successfully
```
#### Decompress
Now it's time to decompress:

**If your original excel file was big and of many rows and columns, it's better and faster to decompress it into a csv file instead of excel directly and then save the file as excel if excel type is necessary. This is because python is not that fast in writing data to excel as well as the tool sometimes has "Corrupted Files" issues with excel.**
```bash
lzhw -d -f "gc_comp.txt" -o "gc_decompressed.csv"

100%|███████████████████████████████████████████████████| 62/62 [00:00<00:00, 690.45it/s]
Creating gc_decompressed.csv file ...
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

100%|███████████████████████████████████████████████████| 62/62 [00:00<00:00, 5651.84it/s]
Creating gc_subset_de.csv file ...
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
Creating gc_subset_de.csv file ...
Decompressed Successfully
```

Here we only decompressed the firt 4 rows, 1-based, including the header.

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

P.S. The tool takes a couple of seconds from 10 to 15 seconds to start working and compressing at the first time and then it runs faster and faster the more you use it. 

