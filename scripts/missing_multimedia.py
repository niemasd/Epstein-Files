#! /usr/bin/env python3
'''
Try to figure out which multimedia files are missing from their accompanying "No Images Produced" PDFs
'''
from pathlib import Path
from pypdf import PdfReader
from sys import stderr, stdout
from tqdm import tqdm
import argparse

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--pdf_dir', required=True, type=str, help="EFTA PDF Directory")
    parser.add_argument('-s', '--min_size', required=False, type=int, default=2433, help="Minimum PDF Size")
    parser.add_argument('-S', '--max_size', required=False, type=int, default=2433, help="Maximum PDF Size")
    parser.add_argument('-t', '--text', required=False, type=str, default="No Images Produced", help="Text to Search For (empty string to skip)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    args = parser.parse_args()
    args.pdf_dir = Path(args.pdf_dir)
    if not args.pdf_dir.is_dir():
        raise ValueError("Directory not found: %s" % args.pdf_dir)
    args.text = args.text.strip().lower()

    # enumerate all EFTA files
    print("Enumerating EFTA files in: %s" % args.pdf_dir, file=stderr)
    efta_files = list(tqdm(args.pdf_dir.rglob('EFTA*.pdf')))

    # count EFTA IDs
    print("Counting EFTA IDs for single-page PDFs...", file=stderr)
    count = dict()
    for path in tqdm(efta_files):
        if '_' not in path.name:
            efta_ID = path.stem.strip().upper()
            if efta_ID not in count:
                count[efta_ID] = 0
            count[efta_ID] += 1

    # find missing multimedia files
    print("Searching for missing multimedia files...", file=stderr)
    missing = list()
    for path in tqdm(efta_files):
        if '_' in path.name or path.suffix.strip().lower() != '.pdf':
            continue
        efta_ID = path.stem.strip().upper()
        if count[efta_ID] != 1:
            continue
        size = path.stat().st_size
        if size < args.min_size or size > args.max_size:
            continue
        if args.text != '':
            with open(path, 'rb') as f:
                if args.text not in PdfReader(f).pages[0].extract_text().lower():
                    continue
        missing.append(path.stem)

    # write output to file
    print("Writing %d missing multimedia files to: %s" % (len(missing), args.output))
    missing.sort()
    if args.output == 'stdout':
        args.output = stdout
    else:
        args.output = open(args.output, 'wt')
    args.output.write('%s\n' % '\n'.join(missing))
    args.output.close()
