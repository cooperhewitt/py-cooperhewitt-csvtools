#!/usr/bin/env python

import csv
import json
import codecs
import cStringIO
import logging

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, **kwds):
        f = UTF8Recoder(f, 'utf-8')
        self.reader = csv.DictReader(f, **kwds)

    def next(self):

        tmp = self.reader.next()
        row = {}

        for k, v in tmp.items():

            try:

                if k == None:
                    logging.error("key is None value which is weird (%s)" % tmp)
                    continue
                if v == None:
                    logging.debug("value is None value (%s)" % tmp)
                    row[ unicode(k, "utf-8") ] = u''                
                else:
                    row[ unicode(k, "utf-8") ] = unicode(v, "utf-8") 
                    
            except Exception, e:

                logging.error("failed to parse line, because %s (%s)" % (e, tmp))

        return row

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, fieldnames, **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, **kwds)
        self.writer.writeheader()
        self.stream = f
        self.encoder = codecs.getincrementalencoder('utf-8')()

    def writerow(self, row):

        enc = {}

        for k, v in row.items():
            if v:
                enc[ k.encode('utf-8') ] = v.encode('utf-8')
            else:
                enc[ k.encode('utf-8') ] = u''

        self.writer.writerow(enc)

        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == '__main__':

    import sys
    import pprint

    logging.basicConfig(level=logging.INFO)

    path = sys.argv[1]
    fh = open(path, 'rU')

    reader = UnicodeReader(fh)

    for row in reader:
        print pprint.pformat(row)

    sys.exit()
