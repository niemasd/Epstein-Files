#! /usr/bin/env python3
'''
Produce the URLs from a directory containing EFTA files
'''
from pathlib import Path
from sys import argv, stderr
URL_BASE = 'https://www.justice.gov/epstein/files/DataSet%20' # append the dataset number + / + EFTA########.pdf
FIRST_DOC = [
    ( '1', 'EFTA00000001'), # https://www.justice.gov/epstein/doj-disclosures/data-set-1-files
    ( '2', 'EFTA00003159'), # https://www.justice.gov/epstein/doj-disclosures/data-set-2-files
    ( '3', 'EFTA00003858'), # https://www.justice.gov/epstein/doj-disclosures/data-set-3-files
    ( '4', 'EFTA00005705'), # https://www.justice.gov/epstein/doj-disclosures/data-set-4-files
    ( '5', 'EFTA00008409'), # https://www.justice.gov/epstein/doj-disclosures/data-set-5-files
    ( '6', 'EFTA00008529'), # https://www.justice.gov/epstein/doj-disclosures/data-set-6-files
    ( '7', 'EFTA00009016'), # https://www.justice.gov/epstein/doj-disclosures/data-set-7-files
    ( '8', 'EFTA00009676'), # https://www.justice.gov/epstein/doj-disclosures/data-set-8-files
    ( '9', 'EFTA00039025'), # https://www.justice.gov/epstein/doj-disclosures/data-set-9-files
    ('10', 'EFTA01262782'), # https://www.justice.gov/epstein/doj-disclosures/data-set-10-files
    ('11', 'EFTA02212883'), # https://www.justice.gov/epstein/doj-disclosures/data-set-11-files
    ('12', 'EFTA02730265'), # https://www.justice.gov/epstein/doj-disclosures/data-set-12-files
]

# get URL from EFTA########.pdf path
def get_url(pdf_path):
    efta = pdf_path.stem.strip().upper()
    for dataset_num, efta_start in sorted(FIRST_DOC, key=lambda x: x[1], reverse=True):
        if efta_start <= efta:
            return URL_BASE + dataset_num + '/' + efta + '.pdf'
    raise ValueError("Unable to determine document URL: %s" % pdf_path)

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <efta_pdf_dir>" % argv[0], file=stderr); exit(1)
    dir_path = Path(argv[1])
    if not dir_path.is_dir():
        raise ValueError("Directory not found: %s" % dir_path)

    # produce URLs
    for pdf_path in dir_path.rglob('EFTA*.pdf'):
        print(get_url(pdf_path))
