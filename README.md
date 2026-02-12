# Epstein-Files
Niema's scripts and files related to the [files released](https://www.justice.gov/epstein/doj-disclosures) as a result of the [Epstein Files Transparency Act (H.R.4405)](https://www.congress.gov/bill/119th-congress/house-bill/4405).

* [`scripts/`](scripts) — This directory contains scripts I wrote to help me automate various tasks related to downloading and organizing the files
* [`missing.txt`](missing.txt) — This is a list of document EFTA IDs I believe I'm missing
    * It assumes that all positive integers between 1 and the maximum EFTA number exist
* [`summary.tsv`](summary.tsv) — This is a spreadsheet summarizing all of the documents I have
    * Files named `EFTAXXXXXXXX_EFTAYYYYYYYY.pdf` were originally named `EFTAXXXXXXXX.pdf`, where `EFTAXXXXXXXX` is the EFTA ID of the first page in the PDF
        * I renamed them to `EFTAXXXXXXXX_EFTAYYYYYYYY.pdf`, where `EFTAYYYYYYYY` is the EFTA ID of the last page in the PDF, to make it easier to track what EFTA IDs exist vs. are missing
    * Files named `EFTAXXXXXXXX_EFTAXXXXXXXX.pdf` (i.e., the same EFTA ID before and after the underscore) were corrupted in the original dataset and were attempted to be repaired here
        * They should be updated if fixed versions are ever released
* [`url_list.txt`](url_list.txt) — This is my (potentially error-prone) complete list of document URLs based on the files I was able to successfully download
    * I created this because the pages directly on the DOJ website can be imperfect and/or difficult to enumerate completely

# Helpful Links

* [Department of Justice Disclosures](https://www.justice.gov/epstein/doj-disclosures)
* [Distributed Denial of Secrets - Epstein Files](https://ddosecrets.org/article/epstein-files)
