#!/usr/bin/env python
import lzhw
import pandas as pd
import argparse
import os
from subprocess import call
from time import time
import multiprocessing


def main():
    ## This script and the solution to convert xlsx into csv was thanks to the answer found here:
    ## https://stackoverflow.com/questions/28766133/faster-way-to-read-excel-files-to-pandas-dataframe
    ## and here: https://stackoverflow.com/questions/1858195/convert-xls-to-csv-on-command-line
    vbscript = """if WScript.Arguments.Count < 3 Then
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

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def csv_reader(file, cols, col_arg, nh_arg):
        if nh_arg:
            h = None
        else:
            h = 0
        if col_arg:
            cols_used = cols.split(",")
            if is_number(cols_used[0]):
                cols_used = [int(i) - 1 for i in cols_used]
        else:
            cols_used = None

        data = pd.read_csv(file, header=h, usecols=cols_used)
        data.columns = list(map(str, data.columns))
        return data

    parser = argparse.ArgumentParser(
        description="LZHW is a tabular data compression tool. It is used to compress excel, csv and any flat file. Version: 0.0.9")
    parser.add_argument("-d", "--decompress", help="decompress input into output",
                        action="store_true", default=False)
    parser.add_argument("-f", "--input", help="input file to be (de)compressed",
                        type=str, required=True)
    parser.add_argument("-o", "--output", help="output where to save result",
                        type=str, required=True)
    parser.add_argument("-c", "--columns", nargs="+",
                        help="select specific columns by names or indices (1-based) to compress or decompress",
                        type=str,
                        required=False)
    parser.add_argument("-r", "--rows",
                        help="select specific rows to decompress (1-based)", type=str,
                        required=False)
    parser.add_argument("-nh", "--no-header", help="skip header / data to be compressed has no header",
                        action="store_true", default=False)
    args = vars(parser.parse_args())

    file = args["input"]
    output = args["output"]

    if args["columns"]:
        cols = args["columns"][0]
    else:
        cols = "all"

    if args["rows"]:
        n_rows = int(args["rows"])
    else:
        n_rows = 0

    if args["decompress"]:
        start = time()
        if cols != "all":
            cols = cols.split(",")
            if is_number(cols[0]):
                cols = [int(i) - 1 for i in cols]

        decompressed = lzhw.decompress_df_from_file(file, cols, n_rows)
        decompressed.fillna("", inplace=True)
        decompressed = decompressed.replace("nan", "", regex=True)
        if "xls" in output:
            # decompressed.reset_index(drop = True, inplace = True)
            options = {}
            options["strings_to_formulas"] = False
            options["strings_to_urls"] = False
            writer = pd.ExcelWriter(output, engine="xlsxwriter", options=options)
            decompressed.to_excel(writer, output.split(".xls")[0], index=False)
            writer.save()
            # decompressed.to_excel(output, index=False, encoding = "utf8")
        if "csv" in output:
            decompressed.to_csv(output, index=False)
        else:
            with open(output, "w") as o:
                decompressed.to_string(o, index=False)
        print("Finalizing Decompression ...")
        print(f"Creating {output} file ...")
        print("time taken: ", (time() - start) / 60, " minutes")
        print("Decompressed Successfully")

    else:
        start = time()
        if "xls" in file:
            print("Reading files, Can take 1 minute or something ...",
                  "\nRunning CScript.exe to convert xls file to csv for better performance", "\n")
            f = open("excel_to_csv.vbs", "w")
            f.write(vbscript)
            f.close()
            csv_file = file.split(".xls")[0] + "1" + ".csv"
            call(["cscript.exe", "excel_to_csv.vbs", file, csv_file, "1"])
            os.remove("excel_to_csv.vbs")

            data = csv_reader(csv_file, cols, args["columns"], args["no_header"])

            os.remove(csv_file)

        elif "csv" in file:
            print("Reading files ...")
            data = csv_reader(file, cols, args["columns"], args["no_header"])

        else:
            with open(file, "r") as i:
                data = i.read()

        comp_df = lzhw.CompressedDF(data)
        print("Finalizing Compression ...")
        comp_df.save_to_file(output)
        print(f"Creating {output} file ...")
        print("time taken: ", (time() - start) / 60, " minutes")
        print("Compressed Successfully")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.Process(target=main).start()
