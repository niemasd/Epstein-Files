#! /usr/bin/env python3
'''
Rename all EFTA files from FIRSTEFTA.pdf to FIRSTEFTA_LASTEFTA.pdf
'''
from pathlib import Path
from pypdf import PdfReader
from re import findall, fullmatch
from tqdm import tqdm
from sys import argv, stderr
PATTERN = 'EFTA[0-9]{8}'

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <folder>" % argv[0], file=stderr); exit(1)
    path = Path(argv[1])
    if not path.is_dir():
        print("Folder not found: %s" % argv[1], file=stderr); exit(1)

    # find all EFTA########.PDF files
    print("Searching for EFTA PDF files in: %s" % path)
    efta_file_paths = sorted(p for p in path.rglob('*.*') if p.name.upper().startswith('EFTA') and p.suffix.lower() == '.pdf')
    print("Found %d EFTA PDF files" % len(efta_file_paths))

    # rename the files
    print("Renaming files...")
    for pdf in tqdm(efta_file_paths):
        if pdf.name.count('EFTA') == 1:
            with open(pdf, 'rb') as f:
                try:
                    pages = PdfReader(f).pages
                    if len(pages) == 1:
                        continue
                    if fullmatch(PATTERN, pdf.stem) is None:
                        min_ID = min(findall(PATTERN, pages[0].extract_text()))
                    else:
                        min_ID = pdf.stem
                    max_ID = max(findall(PATTERN, pages[-1].extract_text()))
                except:
                    raise RuntimeError("Failed to parse PDF: %s" % pdf)
            if min_ID != max_ID:
                dest = pdf.parent / ('%s_%s.pdf' % (min_ID, max_ID))
                if not dest.exists():
                    pdf.rename(dest)
