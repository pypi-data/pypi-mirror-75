#!/usr/bin/python
# -*- coding: utf-8 -*-

__copyright__ = """

MIT License

Copyright (c) 2020 Samapriya Roy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
__license__ = "MIT License"

import csv
import sys
import argparse
from Bio import Entrez

accession_list = []
row_list = []
acession_annotations = []


def merge(lst1, lst2):
    return [a + b for (a, b) in zip(lst1, lst2)]


def accession_parse(path, db, email):
    """This script is intended for annotation of blast results saved in Hit Table CSV format.
       The output is an annotated CSV file "*_annotated.csv" with the following columns added:
       Record name, Species, Date of update, Reference, Full taxonomy

    [description]

    Arguments:
        path {[type]} -- [Pathway to csv-formatted Hit Table file with blast results]
        db {[type]} -- ["For the output of nucleotide blast or tblastn, use 'n'. "
                         "For the output of protein blast or blastx, use 'p'."]
        email {[type]} -- [NCBI email]
    """
    n = 200
    open(path.split(".")[0] + "_annotated.csv", "w")
    with open(path, encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            accession_list.append(row[1])
            row_list.append(row)
    accession_chunk = [
        accession_list[i * n : (i + 1) * n]
        for i in range((len(accession_list) + n - 1) // n)
    ]
    i = 1
    for subsets in accession_chunk:
        idlist = ",".join(subsets)
        Entrez.email = email
        dbdict = {"n": "nuccore", "p": "protein"}
        handle = Entrez.efetch(db=dbdict[db], id=idlist, retmode="xml")
        data = Entrez.parse(handle)
        for items in data:
            try:
                version = items["GBSeq_accession-version"]
                definition = items["GBSeq_definition"]
                organism = items["GBSeq_organism"]
                taxonomy = items["GBSeq_taxonomy"]
                date = items["GBSeq_update-date"]
                ref = ", ".join(items["GBSeq_references"][0]["GBReference_authors"])
                acession_annotations.append(
                    [definition, organism, taxonomy, ref, date]
                )
            except Exception as e:
                version = items["GBSeq_accession-version"]
                definition = items["GBSeq_definition"]
                organism = items["GBSeq_organism"]
                taxonomy = items["GBSeq_taxonomy"]
                date = items["GBSeq_update-date"]
                ref = "No references found"
                acession_annotations.append(
                    [definition, organism, taxonomy, ref, date]
                )
            print("Processed a total of {} records".format(i), end="\r")
            i = i + 1
        handle.close()
        for annotated_rows in merge(row_list, acession_annotations):
            with open(path.split(".")[0] + "_annotated.csv", "a") as csvfile:
                writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                writer.writerow(annotated_rows)
            csvfile.close()
    print('')
    print('Annotated files written to {}'.format(path.split(".")[0] + "_annotated.csv"))

def accession_parse_from_parser(args):
    accession_parse(path=args.path, db=args.db, email=args.email)


def main(args=None):
    parser = argparse.ArgumentParser(description="CLI and utilities for Genetic analysis and database interface")
    subparsers = parser.add_subparsers()
    parser_accession_parse = subparsers.add_parser(
        "blasthit", help="Annotation of blast results saved in Hit Table CSV format"
    )
    parser_accession_parse.add_argument(
        "--path", help="Pathway to csv-formatted Hit Table file with blast results"
    )
    parser_accession_parse.add_argument(
        "--db",
        choices=["n", "p"],
        help="For the output of nucleotide blast or tblastn, use 'n'. "
        "For the output of protein blast or blastx, use 'p'.",
    )
    parser_accession_parse.add_argument("--email", help="NCBI email")
    parser_accession_parse.set_defaults(func=accession_parse_from_parser)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
