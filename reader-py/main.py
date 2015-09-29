__author__ = 'tg'

import nutch_reader as ntc_rdr
from pprint import pprint

## CONFIG BLOCK BEGIN

SEGMENTS_CONTENT_DIR = "/home/tg/work/coursework/cs572/nutch/hw1/try1/segments/*/content/"
CRAWLDB_DIR = "/home/tg/work/coursework/cs572/nutch/hw1/try1/crawldb/current/"
SEG_FETCH_DIR = "/home/tg/work/coursework/cs572/nutch/hw1/try1/segments/*/crawl_fetch/"
GROUP_NAME = "CSCI-572 FALL-15 GROUP-36; Thamme Gowda, Rakshith, Rahul and Nii"

## CONFIG BLOCK END

# task 2c
# Images Mimes
def get_image_mimes():

    # We scan the content directory
    # Scan crawl db for faster and more images
    files = ntc_rdr.find_sequence_files(SEGMENTS_CONTENT_DIR)
    mimes = ntc_rdr.scan_mime_types(files, 1000)
    img_mimes = {}
    for mime, count in mimes.items():
        mime = mime.strip().lower()
        if mime.startswith("image"):
            img_mimes[mime] = count
    return img_mimes


# task 2d, failed urls
def get_failed_urls(n=None):

    """
        Run this command in bash
        nutch readdb try1/crawldb/ -dump ~/tmp/crawldb -status db_gone -format csv
    """
    files = ntc_rdr.find_sequence_files(CRAWLDB_DIR)
    recs = ntc_rdr.seq_reader.read_all(files)
    failure_statuses = {'3 (db_gone)'}
    count = 0
    for k,v in recs:
        status = v.get('Status').strip()
        if status in failure_statuses:
            count += 1
            yield k.toString(), status
            if n and count > n:
                return


def create_report(rep_file):
    import json
    with open(rep_file, 'w') as outf:
        outf.write(GROUP_NAME)
        outf.write("\n\n#2c Image MIMES \n")
        for mime_type,count in get_image_mimes().items():
            outf.write("%s, %d\n" %(mime_type, count))
        outf.write("\n\n")

        outf.write("#2d 100 failed urls\n")
        for url,status in get_failed_urls(n=110):
            outf.write("%s, %s\n" %(url, status))



if __name__ == '__main__':
    create_report("rep.txt")







