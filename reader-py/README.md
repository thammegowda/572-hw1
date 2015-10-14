# nutch_reader
=============
The `nutch_reader.py` performs following two operations:
 + scan image mimes
 + list failed urls

## Scan image mimes:

`
Usage: nutch_reader.py mimes [-h] -r REPORT -db CRAWLDB

optional arguments:
  -h, --help            show this help message and exit
  -r REPORT, --report REPORT
                        Path to report File
  -db CRAWLDB, --crawldb CRAWLDB
                        Path to crawldbs. RegEx is also accepted
`
### Example :

`./nutch_reader.py mimes -r mimes.txt -db /c1/crawldb/current/`


## Dump failed URLS

`
usage: nutch_reader.py failed [-h] [-n NUM_FAILURES] -r REPORT -db CRAWLDB

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_FAILURES, --num-failures NUM_FAILURES
                        Number of failure URLS
  -r REPORT, --report REPORT
                        Path to report File
  -db CRAWLDB, --crawldb CRAWLDB
                        Path to crawldbs. RegEx is also accepted
`

### Examples:

`./nutch_reader.py failed -r mimes.txt -db /c1/crawldb/current/ -n 100`

