import os
import subprocess
import sys
from typing import *
from utils import file_components, sanitize_string
import json
import pandas as pd
import numpy as np
import socket

import urllib.request
import argparse


API_ID = os.environ.get("OXFORD_API_ID")
API_KEY = os.environ.get("OXFORD_API_KEY")

LANG = "en-us"


def get_definition(word: str) -> dict:
    url = f"https://od-api.oxforddictionaries.com:443/api/v2/entries/{LANG}/{word}"
    data = urllib.request.urlopen(url).read().decode("utf-8")
    # data = None
    # try:
    #     data = urllib.request.urlopen(url).read().decode("utf-8")
    # except:
    #     print(f"**Could not get definition for word: {word}")
    # return data


def main():
    parser = argparse.ArgumentParser(
        description="Queries the Oxford Dictionary API for either a list of words or a single word.")
    parser.add_argument("-i", "--input",
                        help="Input file path")
    parser.add_argument("-o", "--output",
                        help="Output file path, leave blank for auto generate", default="")
    parser.add_argument("-s", "--single",
                        help="Input a single word", default="")
    args = parser.parse_args()

    out_path = ""
    definitions = []

    if (args.single != ''):
        word = args.single
        definitions.append(get_definition(word))
    else:
        filepath = args.input

        if (args.output == ''):
            dirpath, filename, ext = file_components(filepath)
            out_path = os.path.join(dirpath, filename + "_OUT") + ".json"
        else:
            out_path = args.output

        with open(filepath, "r") as file:
            for line in file.readlines():
                word = line.strip().lower()
                definition = get_definition(word)
                if (definition != None):
                    definitions.append(definition)

    json.dump(definitions, open(out_path, "w"))


if __name__ == "__main__":
    main()
