#!/usr/bin/env python2.7
# encoding: utf-8
#
# Authors: USC CSCI-572 FALL-2015 GROUP-36
#  ThammeGowda N
#  Rakshith Subramanya
#  Rahul Thankachan
#  Nii Mante


## CONFIG BLOCK BEGIN
__author__ = "USC CSCI-572 FALL-2015 GROUP-36; ThammeGowda, Rakshith, Rahul and Nii"
## CONFIG BLOCK END


from nutchpy import sequence_reader as seq_reader
import os
import argparse
import sys

def scan_mime_types(crawldb):
    '''
    scans all mime types from given segments
    'param: path to crawldb
    :return: key of mime types
    '''
    count = 0
    mimes = {}
    mime_key = 'Content-Type'
    for url,doc in seq_reader.read_all(crawldb):
        #print "# %d :: %s :: %s" % (count, doc.get(mime_key), k)

        # the conversion of sequence file record to python dictionary sometimes fails
        # So defensive programming in action
    
        for k in doc.keys():
            if k and k.startswith(mime_key):
                #print "%s :: %s" %(k, url)
                mime_val = None
                if '=' in k:
                    # then it is of form Content-Type=image/jpeg
                    mime_val = k.split('=')[-1]
                elif k == mime_key:
                    #then the record was properly converted to dictionary
                    mime_val = doc.get(k)

                if mime_val:
                    mime_val = mime_val.strip()
                    if mime_val:
                        #mime val is found, lets update count
                        mimes[mime_val] = mimes.get(mime_val, 0) + 1
                        #print "%s::%s" %(mime_val, url)
                #already found the mimetype of this doc, break the loop        
                break

        count += 1
        if count % 1000 == 0:
            print count
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
    find_cmd = "find %s -maxdepth 5 -type f -regex .*part-[0-9]*/data" % abs_path
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
def get_mimes(segments_path, mime_prefix="image"):
    '''
    Scans segment content for detecting content type
    :param : segments_path - path to segments. This could be regex to match all segment directories
    '''
    # We scan the content directory
    files = find_sequence_files(segments_path)
    mimes = scan_mime_types(files)
    img_mimes = {}
    for mime, count in mimes.items():
        if mime:
            mime = mime.strip().lower()
            if mime.startswith(mime_prefix):
                img_mimes[mime] = count
        else:
            print "Error Mime:Count= %s:%s" %(mime,count)
    return img_mimes


# task 2d, failed urls
def get_failed_urls(crawldb, n=None):
    """
    Gets failure urls from crawldb
    same as nutch command
    ># nutch readdb try1/crawldb/ -dump ~/tmp/crawldb -status db_gone -format csv
    :param : crawldb - path to crawl db
    :param : n - number of failed urls to get. 
    """
    files = find_sequence_files(crawldb)
    recs = seq_reader.read_all(files)
    failure_statuses = {'3 (db_gone)'}
    count = 0
    for k, v in recs:
        if 'Status' in v:
            status = v.get('Status').strip()
            if status in failure_statuses:
                count += 1
                yield k.toString(), status
                if n and count >= n:
                    return
        else:
            print "No Status for %s" % (k)


def create_report(args):
    '''
    Creates report files
    :return: None
    '''
    cmd = args.get('command')
    if cmd == 'failed':
        with open(args['report'], 'w') as outf:
            n = args.get('num_failures')
            outf.write("# %s \n" % __author__)
            outf.write("## 2d. First %d failed urls\n" % n)
            for url,status in get_failed_urls(args['crawldb'], n=n):
                outf.write("%s, %s\n" %(url, status))
                
    elif cmd == 'mimes':
        with open(args['report'], 'w') as outf:
            outf.write("# %s \n" % __author__)
            outf.write("## 2c. Image MIMES \n")
            for mime_type,count in get_mimes(args['crawldb']).items():
                outf.write("%s, %d\n" %(mime_type, count))
    else:
        print "ERROR: Unknown Command : %s" % cmd

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Crawl Stats Reader")

    subparsers = parser.add_subparsers(help ="sub-commands", dest="command")
    fail_parser = subparsers.add_parser("failed", help="dumps failed urls")
    fail_parser.add_argument("-n", "--num-failures", help="Number of failure URLS", default=100, type=int)
    fail_parser.add_argument("-r", "--report", help="Path to report File", required=True)
    fail_parser.add_argument("-db", "--crawldb", help="Path to crawldbs. RegEx is also accepted", required=True)

    mime_parser = subparsers.add_parser("mimes", help="Dumps Image Mimes")
    mime_parser.add_argument("-r", "--report", help="Path to report File", required=True)
    mime_parser.add_argument("-db", "--crawldb", help="Path to crawldbs. RegEx is also accepted", required=True)
    
    args = vars(parser.parse_args(sys.argv[1:]))
    create_report(args)
