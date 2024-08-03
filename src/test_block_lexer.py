from block_lexer import markdown_to_blocks
import unittest


class TestBlockLexer(unittest.TestCase):
    def setUp(self):
        self.simpleBlockOk = [
            (
                """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item""",
                [
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    """* This is the first list item in a list block
* This is a list item
* This is another list item"""
                ]
            ),
            (
                """# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
* This is the first list item in a list block
* This is a list item
* This is another list item""",
                [
                    """# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
* This is the first list item in a list block
* This is a list item
* This is another list item""",
                ]
            ),
            (
                """



# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
* This is the first list item in a list block
* This is a list item
* This is another list item



""",
                [
                    """# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
* This is the first list item in a list block
* This is a list item
* This is another list item""",
                ]
            ),
        ]

    def test_simple_block_ok(self):
        for test, case in self.simpleBlockOk:
            result = markdown_to_blocks(test)
            self.assertListEqual(result, case)
