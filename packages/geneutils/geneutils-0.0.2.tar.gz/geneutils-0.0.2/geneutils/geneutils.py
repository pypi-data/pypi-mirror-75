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
import os
import json
import getpass
import argparse
from os.path import expanduser
from Bio import Entrez

accession_list = []
row_list = []
acession_annotations = []

# Save default NCBI email and API Key
def genauth():
    try:
        email_id = input("Enter your NCBI email address:  ")
        api_key = getpass.getpass("Enter your NCBI API Key:  ")
        if len(api_key) == 0:
            api_key = "pass"
    except Exception as e:
        print(e)

    data = {
        "api_key": api_key.strip(),
        "email": email_id.strip(),
    }

    with open(os.path.join(expanduser("~"), "geneauth.json"), "w") as outfile:
        json.dump(data, outfile)
    if len(data["api_key"]) > 0 and len(data["email"]) > 0:
        print("Credentials created with : email id & api key")


def genauth_from_parser(args):
    genauth()


# Merge lists together
def merge(lst1, lst2):
    return [a + b for (a, b) in zip(lst1, lst2)]


# Get annotate hit table
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

    # get existing credentials
    if os.path.exists(os.path.join(expanduser("~"), "geneauth.json")):
        with open(os.path.join(expanduser("~"), "geneauth.json")) as json_file:
            cred = json.load(json_file)
        email_id = cred["email"]
        api_key = cred["api_key"]

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
        if email != None:
            Entrez.email = email
        elif email is None and len(email_id) > 0:
            Entrez.email = email_id
        if api_key != "pass":
            Entrez.api_key = api_key
        if email is None and len(email_id) > 0 and api_key != "pass":
            print("Using both email and api_key")
        elif email is not None:
            print("Using email id {}".format(email))
        elif email is None and len(email_id) == 0:
            sys.exit("Either pass an email or try geneutils init")
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
                acession_annotations.append([definition, organism, taxonomy, ref, date])
            except Exception as e:
                version = items["GBSeq_accession-version"]
                definition = items["GBSeq_definition"]
                organism = items["GBSeq_organism"]
                taxonomy = items["GBSeq_taxonomy"]
                date = items["GBSeq_update-date"]
                ref = "No references found"
                acession_annotations.append([definition, organism, taxonomy, ref, date])
            print("Processed a total of {} records".format(i), end="\r")
            i = i + 1
        handle.close()
        for annotated_rows in merge(row_list, acession_annotations):
            with open(path.split(".")[0] + "_annotated.csv", "a") as csvfile:
                writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                writer.writerow(annotated_rows)
            csvfile.close()
    print("")
    print("Annotated files written to {}".format(path.split(".")[0] + "_annotated.csv"))


def accession_parse_from_parser(args):
    accession_parse(path=args.path, db=args.db, email=args.email)


def main(args=None):
    parser = argparse.ArgumentParser(
        description="CLI and utilities for Genetic analysis and database interface"
    )
    subparsers = parser.add_subparsers()

    parser_genauth = subparsers.add_parser(
        "init", help="Setup NCBI email and API key as credentials"
    )
    parser_genauth.set_defaults(func=genauth_from_parser)

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
    optional_named = parser_accession_parse.add_argument_group(
        "Optional named arguments"
    )
    optional_named.add_argument(
        "--email", help="NCBI email else from credentials", default=None
    )
    parser_accession_parse.set_defaults(func=accession_parse_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
