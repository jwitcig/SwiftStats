import unittest

from parser import FileObject, CodeLineType, LineItem

class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('/Users/developer/Documents/Projects/SwiftStats/test_data.swift') as f:
            raw_lines = f.readlines()

        cls.parsed_file = FileObject(raw_lines)

    def setUp(self):
        pass

    def test_line_type_creation(self):
        raw_lines = self.parsed_file.raw_lines
        parsed_lines = self.parsed_file.lines

        self.assertEqual(len(raw_lines), len(parsed_lines))
        [self.assertEqual(x.__class__, LineItem) for x in parsed_lines]

    def test_blocks_count(self):
        blocks = self.parsed_file.blocks
        top_level_blocks = self.parsed_file.top_level_blocks

        self.assertEqual(len(top_level_blocks), 4)
        self.assertEqual(len(blocks), 9)

    def test_block_location(self):
        first_block = self.parsed_file.top_level_blocks[0]

        self.assertEqual(range(0, 5), first_block.line_range)

    def test_line_type_count(self):
        types = [x for x in CodeLineType if x.value in ['extension', 'protocol']]

        quantities = {type.value: len(self.parsed_file.lines_of_type(type)) for type in types}

        self.assertEqual(quantities, {'extension': 4, 'protocol': 0})

    def test_code_line_is_type(self):
        is_extension_type = CodeLineType.line_is_type(CodeLineType.extension, 'public static var foodPlace: Location?')
        self.assertFalse(is_extension_type)

        is_protocol_type = CodeLineType.line_is_type(CodeLineType.protocol, 'internal protocol Location {}')
        self.assertTrue(is_protocol_type)

    def test_code_line_type(self):
        code_lines = {
            'public static var foodPlace: Location?': CodeLineType.var,
            'internal protocol Location {}': CodeLineType.protocol,
            'let currentCity: City = City(name: "Jefferson City")': CodeLineType.let,
            'private struct Building {': CodeLineType.struct,
            'private extension Location {}': CodeLineType.extension,
        }

        results = list([CodeLineType.line_type(x) for x in code_lines.keys()])

        self.assertEqual(results, list(code_lines.values()))


    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()
