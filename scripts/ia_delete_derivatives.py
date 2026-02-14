#! /usr/bin/env python3
'''
Delete derivative files from an Internet Archive item
'''

# imports
from internetarchive import get_session
from pathlib import Path
from subprocess import check_output
from sys import stderr
from tqdm import tqdm
import argparse

# constants
SUFFIXES = [
    '_chocr.html.gz',
    '_djvu.txt',
    '_djvu.xml',
    '_hocr.html',
    '_hocr_pageindex.json.gz',
    '_hocr_searchtext.txt.gz',
    '_ia_thumb.jpg',
    '_jp2.zip',
    '_page_numbers.json',
    '_scandata.xml',
]

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', required=False, type=str, default="~/.config/internetarchive/ia.ini", help="Internet Archive CLI Config File")
    parser.add_argument('-i', '--id', required=False, type=str, default='efta_niema', help="Internet Archive Item ID")
    args = parser.parse_args()
    args.config = Path(args.config).expanduser()
    if not args.config.is_file():
        print("File not found: %s" % args.config, file=stderr); exit(1)

    # set up Internet Archive session
    print("Initializing Internet Archive session using: %s" % args.config, file=stderr)
    session = get_session(config_file=args.config)
    print("Getting Internet Archive item: %s" % args.id, file=stderr)
    item = session.get_item(identifier=args.id)

    # find derivative files
    print("Deleting derivative files...")
    for f in tqdm(list(item.get_files())):
        for suffix in SUFFIXES:
            if f.name.endswith(suffix):
                f.delete(); break
