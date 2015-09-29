__author__ = 'ThammeGowda N; USC CSCI-572 Fall-2015 Group-36'


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

if __name__ == '__main__':

    from pprint import pprint
    '''
    segments = ['/home/tg/work/coursework/cs572/nutch/hw1/try1/segments/20150921003734/content/part-00001/data']
    mimes = scan_mime_types(segments, batch_size=100)
    pprint(mimes)

    '''
    """
    mimes = scan_mime_types(files, batch_size=50)
    pprint(mimes)
    """

    files = find_sequence_files("/home/tg/work/coursework/cs572/nutch/hw1//try2/crawl/segments/20150926144008/content/")
    print "%d sequence files" % len(files)
    mimes = scan_mime_types([files[1]])
    pprint(mimes)




