* [`clean.py`](clean.py) — Delete files that are probably the result of failed download attempts (e.g. error pages, 0-byte files, etc.)
* [`download.py`](download.py) — Bulk-download documents from a list of EFTA IDs
* [`extract_efta.sh`](extract_efta.sh) — Extract EFTA IDs from a given PDF using `pdftotext`
* [`infer_urls.py`](infer_urls.py) — Infer document URLs that probably exist on the DOJ website given a collection of downloaded PDFs
* [`missing.py`](missing.py) — Produce a list of document EFTA IDs that are probably missing from a given collection of downloaded PDFs
    * This script assumes that documents exist with all possible EFTA numbers from 1 to the maximum value in the collection
    * You should make sure to manually download the single document with the largest EFTA number and include it in your collection
* [`rename.py`](rename.py) — Rename multi-page PDFs from `EFTAXXXXXXXX.pdf` to `EFTAXXXXXXXX_EFTAYYYYYYYY.pdf`
    * `EFTAXXXXXXXX` is the EFTA ID of the first page in the PDF
    * `EFTAYYYYYYYY` is the EFTA ID of the last page in the PDF
    * The original PDFs are named `EFTAXXXXXXXX.pdf`, even if they contain multiple documents with different EFTA IDs
    * This script infers `EFTAXXXXXXXX` as the smallest EFTA number on the first page, and it infers `EFTAYYYYYYYY` as the largest EFTA number on the last page
        *  This could be incorrect, as some documents embed other documents (and thus their EFTA IDs)
        *  You can use [`missing.py`](missing.py) to check for cases where this script inferred incorrect EFTA IDs
