#!/usr/bin/env python2.7
# encoding: utf-8
#
# Authors: USC CSCI-572 FALL-2015 GROUP-36
#  ThammeGowda N
#  Rakshith Subramanya
#  Rahul Thankachan
#  Nii Mante



## CONFIG BLOCK BEGIN

SEGMENTS_CONTENT_DIR = "/home/tg/work/coursework/cs572/hw1/sites/armslist/c1/merged/*/content/"
CRAWLDB_DIR = "/home/tg/work/coursework/cs572/hw1/sites/armslist/c1/crawldb/current/"
GROUP_NAME = "USC CSCI-572 FALL-2015 GROUP-36; ThammeGowda, Rakshith, Rahul and Nii"

## CONFIG BLOCK END


from nutchpy import sequence_reader as seq_reader
import os

def scan_mime_types(segment_paths, limit=None):
    '''
    scans all mime types from given segments
    :return: key of mime types
    '''
    count = 0
    mimes = {}
    for k,doc in seq_reader.read_all(segment_paths, limit=limit):
        #print "# %d :: %s :: %s" % (count, doc.get("contentType"), k)
        count += 1
        mimes[doc.get('contentType')] = mimes.get(doc.get('contentType', 'unknown/unknown'), 0) + 1
    mimes["__total__"] = count
    return mimes


def find_sequence_files(path):

    """
    Finds all the parts of sequence files
    :param path: the root path
    :return: list of paths
    """

    abs_path = os.path.abspath(path)
    #WARNING: this works only in Unix environment
    find_cmd = "find %s -maxdepth 10 -type f -regex .*part-[0-9]*/data" % abs_path
    import subprocess
    out = subprocess.Popen(find_cmd, shell=True, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Get standard out and error
    (stdout, stderr) = out.communicate()
    if 0 != out.returncode:
        raise Exception(stderr.decode())
    return stdout.decode().split()

# task 2c
# Images Mimes
def get_image_mimes():
    # We scan the content directory
    # Scan crawl db for faster and more images
    files = find_sequence_files(SEGMENTS_CONTENT_DIR)
    mimes = scan_mime_types(files, 1000)
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
    files = find_sequence_files(CRAWLDB_DIR)
    recs = seq_reader.read_all(files)
    failure_statuses = {'3 (db_gone)'}
    count = 0
    for k,v in recs:
        if 'Status' in v:
            status = v.get('Status').strip()
            if status in failure_statuses:
                count += 1
                yield k.toString(), status
        else:
            print "No Status for %s" % (k)
        if n and count > n:
            return


def create_report(bad_urls_file, mime_types_file):
    '''
    Creates report files
    :param bad_urls_file: path to file where failed urls needs to be saved
    :param mime_types_file: path to file where image mimes needs to be saved
    :return:
    '''
    with open(mime_types_file, 'w') as outf:
        outf.write("#2c Image MIMES \n")
        for mime_type,count in get_image_mimes().items():
            outf.write("%s, %d\n" %(mime_type, count))

    with open(bad_urls_file, 'w') as outf:
        outf.write("#2d 100 failed urls\n")
        for url,status in get_failed_urls(n=110):
            outf.write("%s, %s\n" %(url, status))


if __name__ == '__main__':
    create_report("bad_urls.txt", "image_mimes.txt")