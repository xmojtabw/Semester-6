#!/usr/bin/env python

import argparse
from argcomplete import autocomplete



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample script with autocomplete")
    autocomplete(parser)
    parser.add_argument("--name", help="Your name")
    parser.add_argument("--age", type=int, help="Your age")
    parser.add_argument("--gender", choices=["male", "female", "other"], help="Your gender")
    parser.add_argument("files", nargs="+", help="Files to process")
    
    args = parser.parse_args()
    print(args)