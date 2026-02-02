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
    parser.add_argument('-s', '--size_threshold', required=False, type=int, default=3000, help="PDF Check Size Threshold")
    parser.add_argument('-t', '--text', required=False, type=str, default="No Images Produced", help="Text to Search For")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    args = parser.parse_args()
    args.pdf_dir = Path(args.pdf_dir)
    if not args.pdf_dir.is_dir():
        raise ValueError("Directory not found: %s" % args.pdf_dir)
    query = args.text.strip().lower()
    if args.output == 'stdout':
        args.output = stdout
    else:
        args.output = open(args.output, 'wt')

    # find missing multimedia files
    print("Scanning EFTA PDF files in: %s" % args.pdf_dir, file=stderr)
    for pdf_path in tqdm(sorted(args.pdf_dir.rglob('EFTA*.pdf'))):
        if ('_' not in pdf_path.name) and (pdf_path.stat().st_size <= args.size_threshold):
            with open(pdf_path, 'rb') as f:
                if (query in PdfReader(f).pages[0].extract_text().lower()) and (len(list(pdf_path.parent.rglob('%s*' % pdf_path.stem))) == 1):
                    print(pdf_path.stem, file=args.output)
    args.output.close()
