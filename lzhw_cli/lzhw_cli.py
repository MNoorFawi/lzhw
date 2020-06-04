#!/usr/bin/env python

import lzhw
import pandas as pd
import argparse
import csv
import os

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
parser.add_argument("-nh", "--no-header", help="skip header / data has no header",
                    action="store_true", default=False)
args = vars(parser.parse_args())

file = args["input"]
output = args["output"]

if args["columns"]:
    cols = args["columns"][0]#.split(",")
else:
    cols = "all"

if args["decompress"]:
    if cols != "all":
        cols = [int(i) - 1 for i in cols.split(",")]
    decompressed = lzhw.decompress_df_from_file(file, cols)
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
        if args["columns"]:
            command = f"in2csv {file} | csvcut -c {cols}"
            csvdf = csv.reader(os.popen(command).read().splitlines())
            if args["no_header"]:
                h = None
            else:
                h = next(csvdf)
            data = pd.DataFrame(csvdf, columns=h)
        else:
            data = pd.read_excel(file)

    elif "csv" in file:
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
