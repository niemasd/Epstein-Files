#! /usr/bin/env python3
'''
Produce a summary TSV from a directory of EFTA files
'''
from pathlib import Path
from tqdm import tqdm
from sys import argv, stderr
HEADER = ['name', 'size']

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <folder>" % argv[0], file=stderr); exit(1)
    path = Path(argv[1])
    if not path.is_dir():
        print("Folder not found: %s" % argv[1], file=stderr); exit(1)

    # find all EFTA########.PDF files
    print("Searching for EFTA files in: %s" % path, file=stderr)
    efta_file_paths = sorted(path.rglob('EFTA*.*'))
    print("Found %d EFTA files" % len(efta_file_paths), file=stderr)

    # produce summary
    print('\t'.join(HEADER))
    for file_path in tqdm(efta_file_paths):
        row = list()
        for k in HEADER:
            if k == 'name':
                row.append(file_path.name)
            elif k == 'size':
                row.append(str(file_path.stat().st_size))
            else:
                raise KeyError("Invalid header key: %s" % k)
        print('\t'.join(row))
