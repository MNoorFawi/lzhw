#!/usr/bin/env python

import lzhw
import pandas as pd
import argparse
import csv
import os
from subprocess import call

## This script and the solution to convert xlsx into csv was thanks to the answer found here:
## https://stackoverflow.com/questions/28766133/faster-way-to-read-excel-files-to-pandas-dataframe
## and here: https://stackoverflow.com/questions/1858195/convert-xls-to-csv-on-command-line
vbscript="""if WScript.Arguments.Count < 3 Then
    WScript.Echo "Please specify the source and the destination files. Usage: ExcelToCsv <xls/xlsx source file> <csv destination file> <worksheet number (starts at 1)>"
    Wscript.Quit
End If

csv_format = 6

Set objFSO = CreateObject("Scripting.FileSystemObject")

src_file = objFSO.GetAbsolutePathName(Wscript.Arguments.Item(0))
dest_file = objFSO.GetAbsolutePathName(WScript.Arguments.Item(1))
worksheet_number = CInt(WScript.Arguments.Item(2))

Dim oExcel
Set oExcel = CreateObject("Excel.Application")

Dim oBook
Set oBook = oExcel.Workbooks.Open(src_file)
oBook.Worksheets(worksheet_number).Activate

oBook.SaveAs dest_file, csv_format

oBook.Close False
oExcel.Quit
"""

parser = argparse.ArgumentParser(description="Data Frame Compressor")
parser.add_argument("-d", "--decompress", help="decompress input into output",
                    action="store_true", default=False)
parser.add_argument("-f", "--input", help="input file to be (de)compressed",
                    type=str, required=True)
parser.add_argument("-o", "--output", help="output where to save result",
                    type=str, required=True)
parser.add_argument("-c", "--columns", nargs="+",
                    help="select specific columns by names or indices (1-based)", type=str,
                    required=False)
parser.add_argument("-r", "--rows",
                    help="select specific rows to decompress (1-based)", type=str,
                    required=False)
parser.add_argument("-nh", "--no-header", help="skip header / data has no header",
                    action="store_true", default=False)
args = vars(parser.parse_args())

file = args["input"]
output = args["output"]

if args["columns"]:
    cols = args["columns"][0]#.split(",")
else:
    cols = "all"

if args["rows"]:
    n_rows = int(args["rows"])
else:
    n_rows = 0

if args["decompress"]:
    if cols != "all":
        cols = [int(i) - 1 for i in cols.split(",")]
    decompressed = lzhw.decompress_df_from_file(file, cols, n_rows)
    if "xls" in output:
        decompressed.to_excel(output, index=False)
    if "csv" in output:
        decompressed.to_csv(output, index=False)
    else:
        with open(output, "w") as o:
            decompressed.to_string(o, index=False)
    print("decompressed successfully")

else:
    if "xls" in file:
        print("Reading files, Can take 1 minute or something ...")
        f = open("excel_to_csv.vbs", "w")
        f.write(vbscript)
        f.close()
        csv_file = file.split(".xls")[0] + "1" + ".csv"
        call(["cscript.exe", "excel_to_csv.vbs", file, csv_file, "1"])
        os.remove("excel_to_csv.vbs")
        if args["columns"]:
            command = f"csvcut -c {cols} {csv_file}"
            csvdf = csv.reader(os.popen(command).read().splitlines())
            if args["no_header"]:
                h = None
            else:
                h = next(csvdf)
            data = pd.DataFrame(csvdf, columns=h)
        else:
            data = pd.read_csv(csv_file)
        os.remove(csv_file)

    elif "csv" in file:
        print("Reading files ...")
        if args["columns"]:
            command = f"csvcut -c {cols} {file}"
            csvdf = csv.reader(os.popen(command).read().splitlines())
            if args["no_header"]:
                h = None
            else:
                h = next(csvdf)
            data = pd.DataFrame(csvdf, columns=h)
        else:
            data = pd.read_csv(file)

    else:
        with open(file, "r") as i:
            data = i.read()

    comp_df = lzhw.CompressedDF(data)
    comp_df.save_to_file(output)
    print("compressed successfully")
