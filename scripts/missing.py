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

# constants
BOUNDS = [ # (dataset, start, end) tuples
    ( '1', 'EFTA00000001', 'EFTA00003158'), # https://www.justice.gov/epstein/doj-disclosures/data-set-1-files?page=63
    ( '2', 'EFTA00003159', 'EFTA00003857'), # https://www.justice.gov/epstein/doj-disclosures/data-set-2-files?page=11
    ( '3', 'EFTA00003858', 'EFTA00005704'), # https://www.justice.gov/epstein/doj-disclosures/data-set-3-files?page=1
    ( '4', 'EFTA00005705', 'EFTA00008408'), # https://www.justice.gov/epstein/doj-disclosures/data-set-4-files?page=3
    ( '5', 'EFTA00008409', 'EFTA00008528'), # https://www.justice.gov/epstein/doj-disclosures/data-set-5-files?page=2
    ( '6', 'EFTA00008529', 'EFTA00009015'), # https://www.justice.gov/epstein/doj-disclosures/data-set-6-files
    ( '7', 'EFTA00009016', 'EFTA00009675'), # https://www.justice.gov/epstein/doj-disclosures/data-set-7-files
    ( '8', 'EFTA00009676', 'EFTA00039024'), # https://www.justice.gov/epstein/doj-disclosures/data-set-8-files?page=220
    ( '9', 'EFTA00039025', 'EFTA00377003'), # https://www.justice.gov/epstein/doj-disclosures/data-set-9-files?page=1437
    ('10', 'EFTA01262782', 'EFTA01925959'), # https://www.justice.gov/epstein/doj-disclosures/data-set-10-files?page=6055
    ('11', 'EFTA02212883', 'EFTA02340018'), # https://www.justice.gov/epstein/doj-disclosures/data-set-11-files?page=1499
    ('12', 'EFTA02730265', 'EFTA02731789'), # https://www.justice.gov/epstein/doj-disclosures/data-set-12-files?page=3
]

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', type=str, required=False, default='stdout', help="Output File")
    parser.add_argument('-p', '--check_pdf', action='store_true', help="Check PDF Lengths (slow)")
    parser.add_argument('-e', '--exhaustive', action='store_true', help="Exhaustively List EFTAs from 1 to Max")
    parser.add_argument('file_dir', nargs='*', help="Directories Containing EFTA######## Files")
    args = parser.parse_args()
    paths = [Path(d) for d in args.file_dir]
    if len(paths) == 0:
        paths = [Path('.')] # default to current directory if no paths given

    # enumerate all EFTA########.* files
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
        if args.check_pdf: #and p.suffix.strip().lower() == '.pdf':
            with open(p, 'rb') as pdf_file:
                pdf_num_pages = len(PdfReader(pdf_file).pages)
            if len(curr_nums) != pdf_num_pages:
                print("ERROR: Filename doesn't match number of PDF pages: %s" % p, file=stderr); exit(1)
        size_pre = len(efta_nums)
        efta_nums |= curr_nums
        size_post = len(efta_nums)
        if size_pre + len(curr_nums) != size_post:
            print("\n\nERROR: Overlapping EFTA numbers: %s" % p, file=stderr); exit(1)

    # enumerate all possible EFTA numbers
    print("Determining all possible EFTA numbers...")
    if args.exhaustive:
        possible_nums = range(1, max(int(BOUNDS[-1][2].replace('EFTA','')), max(efta_nums)) + 1)
    else:
        possible_nums = sorted({num for dataset, start, end in BOUNDS for num in range(int(start.replace('EFTA','')), int(end.replace('EFTA','')) + 1)})

    # print missing EFTA numbers
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
