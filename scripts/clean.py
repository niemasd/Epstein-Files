#! /usr/bin/env python3
'''
Remove all failed downloads
'''
from pathlib import Path
from sys import argv, stderr
from tqdm import tqdm
PREFIX = b'<HTML><HEAD>\n'
PREFIX_LEN = len(PREFIX)

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <folder>" % argv[0], file=stderr); exit(1)
    path = Path(argv[1])
    if not path.is_dir():
        print("Folder not found: %s" % argv[1], file=stderr); exit(1)

    # remove all empty-looking files
    for pdf in tqdm(path.rglob('EFTA*.*')):
        with open(pdf, 'rb') as f:
            prefix = f.read(13)
        if len(prefix) < PREFIX_LEN or prefix == PREFIX:
            pdf.unlink()
