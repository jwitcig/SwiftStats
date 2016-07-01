from enum import Enum
from interval import Interval, IntervalSet
import re
import sys

def range_contains(range, subset):
    return set(subset).issubset(set(range))

class FileObject(object):
    raw_lines = None
    blocks = None

    lines = None

    def __init__(self, raw_lines):
        self.raw_lines = raw_lines
        self.blocks = self.find_brace_pairs()

        self.lines = self.generate_line_items()

    def line_range(self):
        return range(0, self.line_count)

    @property
    def line_count(self):
        return len(self.raw_lines)

    def lines_of_type(self, type, range=None):
        if range is None:
            range = self.line_range
        return [x for x in self.lines if CodeLineType.line_is_type(type, x.raw)]

    @property
    def top_level_blocks(self):
        return [x for x in self.blocks if x.parent_block == None]

    def find_brace_pairs(self):
        raw_lines = self.raw_lines
        bracket_blocks = []

        open_brackets = []
        for index, line in enumerate(raw_lines):
            bracket_index = line.find('{')
            if not bracket_index == -1:
                open_brackets.append((line, index))

            if not line.find('}') == -1:
                (open_line, open_line_index) = open_brackets[-1]
                del open_brackets[-1]
                bracket_blocks.append(BracketBlock(open_line_index, index, self))
        return bracket_blocks

    @property
    def white_lines_count(self):
        return len([x for x in self.lines if x.is_white_line])

    def clean(self):
        self.raw_lines = [x.raw for x in self.lines if not x.is_white_line]
        self.lines = self.generate_line_items()

    def generate_line_items(self):
        return [LineItem(x) for x in self.raw_lines]

class BracketBlock(object):
    first_line_index = None
    last_line_index = None
    file = None

    def __init__(self, first_line_index, last_line_index, file):
        self.first_line_index = first_line_index
        self.last_line_index = last_line_index
        self.file = file

    @property
    def raw_lines(self):
        return self.file.raw_lines[first_line_index:last_line_index]

    @property
    def lines(self):
        return self.file.lines[first_line_index:last_line_index]

    @property
    def line_range(self):
        return range(self.first_line_index, self.last_line_index)

    @property
    def first_line(self):
        return self.file.lines[first_line_index]

    @property
    def last_line(self):
        return self.file.lines[last_line_index]

    def lines_of_type(self, type):
        return self.file.lines_of_type(type, range=self.line_range)

    @property
    def owned_lines(self):
        owned_blocks = [x for x in self.contained_blocks if x.parent_block == self]

        parent_interval_set = IntervalSet(Interval(self.line_range[0], self.line_range[-1]))
        child_intervals_set = IntervalSet([Interval(x.line_range[0], x.line_range[-1]) for x in owned_blocks])
        return parent_interval - child_intervals_set

    @property
    def contained_blocks(self):
        blocks = [x for x in self.file.blocks if range_contains(self.line_range, x)]
        return blocks.sort()

    # @property
    # def contained_blocks(self):
    #     contained_blocks = []
    #     for block in self.file.blocks:
    #         child_block_line_range = range(block.first_line_index, block.last_line_index)
    #
    #         if range_contains(self.line_range, child_block_line_range):
    #             contained_blocks.append(block)
    #     return contained_blocks

    @property
    def parent_block(self):
        potential_blocks = [x for x in self.file.blocks if x is not self]
        try:
            return [x for x in potential_blocks if range_contains(x.line_range, self.line_range)][-1]
        except IndexError:
            return None

    @property
    def open_brace_index(self):
        return self.first_line.find('{')

    @property
    def close_brace_index(self):
        return self.last_line.find('}')

class LineItem(object):
    raw = None

    def __init__(self, raw_line):
        self.raw = raw_line

    @property
    def is_white_line(self):
        if len(self.raw) == 0:
            return True
        return self.raw == '\n'

    @property
    def split_line_into_words(line):
        replacables = [
            ('<', ' < '),
            ('>', '> '),
            (':', ' : '),
            ('{', ''),
            ('}', ''),
        ]

        for removable, replacable in replacables:
            line = str.replace(line, removable, replacable)
        return [word for word in line.split()]

class Publicity(Enum):
    public = 'public'
    private = 'private'
    internal = 'internal'

class CodeLineType(Enum):
    let = 'let'
    var = 'var'

    protocol = 'protocol'
    extension = 'extension'

    # class_declaration ('class' is a protected keyword)
    class_dec = 'class'
    struct = 'struct'

    def line_type(raw_line):
        for type in CodeLineType:
            if CodeLineType.line_is_type(type, raw_line):
                return type
        return None

    def line_is_type(type, raw_line):
        return re.search(r'(?<=\s)*('+type.value+')(?=\s)', raw_line) is not None

def parse_file(file_path):

    with open(file_path) as f:
        raw_lines = f.readlines()

    return FileObject(raw_lines)


# parse_file(sys.argv[1])
