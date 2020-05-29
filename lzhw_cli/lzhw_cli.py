#!/usr/bin/env python

import lzhw
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Data Frame Compressor")
parser.add_argument("-d", "--decompress", help="decompress input into output",
                    action="store_true", default=False)
parser.add_argument("-f", "--input", help="input file to be (de)compressed",
                    type=str, required=True)
parser.add_argument("-o", "--output", help="output where to save result",
                    type=str, required=True)
args = vars(parser.parse_args())

file = args["input"]
output = args["output"]

if args["decompress"]:
    decompressed = lzhw.decompress_df_from_file(file)
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
        data = pd.read_excel(file)
    if "csv" in file:
        data = pd.read_csv(file)
    else:
        with open(file, "r") as i:
            data = i.read()

    comp_df = lzhw.CompressedDF(data)
    comp_df.save_to_file(output)
    print("compressed successfully")
