from block_lexer import markdown_to_blocks, block_to_block_type
from blocknode import BlockNodeType
import unittest


class TestBlockLexer(unittest.TestCase):
    def setUp(self):
        self.simple_block_test = [
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
        self.block_type_test = [
            (
                "# this is a heading",
                BlockNodeType.HEADER
            ),
            (
                "## this is a heading",
                BlockNodeType.HEADER
            ),
            (
                "# # this is a heading",
                BlockNodeType.HEADER
            ),
            (
                "### this is a heading",
                BlockNodeType.HEADER
            ),
            (
                "###### this is a heading",
                BlockNodeType.HEADER
            ),
            (
                "####### this is a heading",
                BlockNodeType.PARAGRAPH
            ),
            (
                " this is a heading",
                BlockNodeType.PARAGRAPH
            ),
            (
                "##this is a heading",
                BlockNodeType.PARAGRAPH
            ),
            (
                """* This is the first list item in a list block
* This is a list item
* This is another list item""",
                BlockNodeType.ULIST
            ),
            (
                """- This is the first list item in a list block
- This is a list item
- This is another list item""",
                BlockNodeType.ULIST
            ),
            (
                """ This is the first list item in a list block
- This is a list item
- This is another list item""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """* This is the first list item in a list block
 This is a list item
* This is another list item""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """1. This is the first list item in a list block
2. This is a list item
3. This is another list item""",
                BlockNodeType.OLIST
            ),
            (
                """1. This is the first list item in a list block
. This is a list item
3. This is another list item""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """1. This is the first list item in a list block
3. This is a list item
2. This is another list item""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """. This is the first list item in a list block
3. This is a list item
2. This is another list item""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """``` This is the first list item in a list block
3. This is a list item
2. This is another list item```""",
                BlockNodeType.CODE
            ),
            (
                """``` This is the first list item in a list block
3. This is a list item
2. This is another list item```@""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """`` This is the first list item in a list block
3. This is a list item
2. This is another list item```""",
                BlockNodeType.PARAGRAPH
            ),
            (
                """> This is the first list item in a list block
>This is a list item
>This is another list item""",
                BlockNodeType.QUOTE
            ),
            (
                """> This is the first list item in a list block
This is a list item
>This is another list item""",
                BlockNodeType.PARAGRAPH
            ),
        ]

    def test_simple_block_ok(self):
        for test, case in self.simple_block_test:
            result = markdown_to_blocks(test)
            self.assertListEqual(result, case)

    def test_block_type_ok(self):
        for test, case in self.block_type_test:
            result = block_to_block_type(test)
            self.assertEqual(result, case)
