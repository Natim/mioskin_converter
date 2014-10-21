import sys, csv, codecs

PY3 = sys.version > '3'

class UnicodeReader:
    def __init__(self, input_file, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.f = input_file
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw
        self.reader = csv.reader(self.f, dialect=self.dialect,
                                 **self.kw)
        
    def next(self):
        row = next(self.reader)
        if PY3:
            return row
        return [s.decode("utf-8") for s in row]
    
    __next__ = next

    def __iter__(self):
        return self


class UnicodeWriter:
    def __init__(self, output_file, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.f = output_file
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw
        self.writer = csv.writer(self.f, dialect=self.dialect,
                                 **self.kw)

    def writerow(self, row):
        if not PY3:
            row = [s.encode(self.encoding) for s in row]
        self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
