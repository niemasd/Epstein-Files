#! /usr/bin/env python3
'''
List the missing PDF files
'''
from gzip import open as gopen
from pathlib import Path
from pypdf import PdfReader
from sys import stderr
from tqdm import tqdm
import argparse
MAX_EFTA = 2731789

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', type=str, required=False, default='stdout', help="Output File")
    parser.add_argument('-p', '--check_pdf', action='store_true', help="Check PDF Lengths (slow)")
    parser.add_argument('file_dir', nargs='*', help="Directories Containing EFTA########.pdf Files")
    args = parser.parse_args()
    paths = [Path(d) for d in args.file_dir]
    if len(paths) == 0:
        paths = [Path('.')] # default to current directory if no paths given

    # enumerate all EFTA########.pdf files
    efta_file_paths = list()
    for dir_path in paths:
        print("Finding EFTA files in: %s" % dir_path, file=stderr)
        efta_file_paths += list(tqdm(dir_path.rglob('EFTA*.pdf')))

    # get all EFTA numbers that are in the dataset
    efta_nums = set()
    print("Searching for missing EFTA files...", file=stderr)
    for p in tqdm(efta_file_paths):
        if '_' in p.stem:
            x, y = [int(part) for part in p.stem.replace('EFTA','').split('_')]
            curr_nums = set(range(x, y+1))
        else:
            curr_nums = {int(p.stem.replace('EFTA',''))}
        if args.check_pdf:
            with open(p, 'rb') as pdf_file:
                pdf_num_pages = len(PdfReader(pdf_file).pages)
            if len(curr_nums) != pdf_num_pages:
                print("ERROR: Filename doesn't match number of PDF pages: %s" % p, file=stderr); exit(1)
        size_pre = len(efta_nums)
        efta_nums |= curr_nums
        size_post = len(efta_nums)
        if size_pre + len(curr_nums) != size_post:
            print("\n\nERROR: Overlapping EFTA numbers: %s" % p, file=stderr); exit(1)

    # print missing EFTA numbers
    possible_nums = range(1, max(MAX_EFTA, max(efta_nums)) + 1)
    if args.output == 'stdout':
        from sys import stdout as out_file
    elif args.output.strip().lower().endswith('.gz'):
        out_file = gopen(args.output, 'wt')
    else:
        out_file = open(args.output, 'wt')
    for num in possible_nums:
        if num not in efta_nums:
            print("EFTA" + str(num).zfill(8), file=out_file)
    out_file.close()
