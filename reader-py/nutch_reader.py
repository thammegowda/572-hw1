__author__ = 'ThammeGowda N; USC CSCI-572 Fall-2015 Group-36'


from nutchpy import sequence_reader as seq_reader


def scan_mime_types(segment_paths, batch_size=20, limit=None):
    '''
    scans all mime types from given segments
    :return: key of mime types
    '''
    count = 1
    mimes = {}
    for k,doc in read_segments(segment_paths, batch_size=batch_size, limit=limit):
        #print "# %d :: %s :: %s" % (count, doc.get("contentType"), k)
        count += 1
        mimes[doc.get('contentType')] = mimes.get(doc.get('contentType', 'unknown/unknown'), 0) + 1
    mimes["__total__"] = count
    return mimes


def read_segments(segment_paths, start=0, batch_size=20, limit=None):
    '''
    Reads a stream of documents from all the segments
    :param segment_paths: list of segment paths
    :param start the starting position
    :param batch_size: buffer size
    :return: stream of records
    '''
    count = 0
    for seg in segment_paths:
        for rec in slice_read(seq_reader, seg, start, batch_size):
            count += 1
            if limit and count > limit:
                return
            yield rec

def rec_to_doc(rec):
    '''
    Converts the sequence file record into (k, doc) pair
    :param rec: record read from sequence file
    :return: tuple containing (rec[0], dict(rec(1)))
    '''
    if len(rec) != 2:
        raise Exception("Expected input: [key,value], given=%s" % rec)
    datum = rec[1]
    parts = datum.split("\n")
    doc = {}
    for part in parts:
        splits = part.strip().split(":", 1)
        if len(splits) > 1:
            doc[splits[0]] = splits[1]
    return (rec[0], doc)

def slice_read(reader, path, start=0, batch_size=20):
    '''
    Reads the sequence file records by slicing batch by batch.
    This was written as a worker around for reader.read(...) freeze issue
    :param reader: the reader which support slice() operation
    :param path: path of the file
    :param start: the start position, default is 0
    :param batch_size: back size default is 20
    :return: iterator of records
    '''
    max = reader.count(path)
    while start < max:
        batch = reader.slice(start, start + batch_size, path)
        for item in batch:
            yield rec_to_doc(item)
        start = start + batch_size

if __name__ == '__main__':
    segments = ['/home/tg/work/coursework/cs572/nutch/hw1/try1/segments/20150920210745/content/part-00001/data']
    mimes = scan_mime_types(segments, batch_size=100)
    from pprint import pprint
    pprint(mimes)