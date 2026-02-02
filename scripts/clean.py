#! /usr/bin/env python3
'''
Remove all failed downloads
'''
from pathlib import Path
from sys import argv, stderr
from tqdm import tqdm
PREFIXES = [b'<HTML><HEAD>\n', b'\n\n<!DOCTYPE html>\n']

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <folder>" % argv[0], file=stderr); exit(1)
    path = Path(argv[1])
    if not path.is_dir():
        print("Folder not found: %s" % argv[1], file=stderr); exit(1)

    # remove all empty-looking files
    for pdf in tqdm(list(path.rglob('EFTA*.*'))):
        with open(pdf, 'rb') as f:
            prefix = f.read(100)
        delete = False
        if len(prefix) == 0:
            delete = True
        else:
            for PREFIX in PREFIXES:
                if prefix.startswith(PREFIX):
                    delete = True
        if delete:
            pdf.unlink()
