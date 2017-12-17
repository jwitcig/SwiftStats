import re

class LineStats(object):

    line = None

    def __init__(line_item):
        self.line = line_item

    @property
    def variables_declared(self):
        # term is preceded by start of line OR whitespace. Succeeded by one or more whitespaces
        re.search(r'(^|(?<=\s))('+x.value+')(?=\s+)', self.line.raw)
