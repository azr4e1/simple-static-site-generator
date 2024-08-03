import unittest
from unittest import TestCase
from textnode import TextNode, TextNodeType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(TestCase):
    def setUp(self):
        self.textNodeEqual = [
            (TextNode("", "ciao", None), TextNode("", "ciao", None)),
            (TextNode("ok", "", "ok"), TextNode("ok", "", "ok")),
            (TextNode("", "c"), TextNode("", "c")),
        ]
        self.textNodeUnequal = [
            (TextNode("", "ciao", None), TextNode("", "cia", None)),
            (TextNode("ok", "", "ok"), TextNode("ok", "", None)),
            (TextNode("okkk", "c"), TextNode("", "c")),
        ]
        self.text_to_html = [
            (TextNode("ciao", TextNodeType.BOLD), LeafNode('ciao', "b")),
            (TextNode("ciao", TextNodeType.BOLD, "github.com"), LeafNode('ciao', 'b')),
            (TextNode("ciao", TextNodeType.ITALIC), LeafNode('ciao', 'i')),
            (TextNode("ciao", TextNodeType.CODE), LeafNode('ciao', 'code')),
            (TextNode("ciao", TextNodeType.TEXT), LeafNode("ciao")),
            (TextNode("ciao", TextNodeType.IMAGE), LeafNode(
                'ciao', 'img', {'src': '', 'alt': 'ciao'})),
            (TextNode("ciao", TextNodeType.IMAGE, "github.com"),
             LeafNode('ciao', 'img', {'src': 'github.com', 'alt': 'ciao'})),
            (TextNode("ciao", TextNodeType.LINK),
             LeafNode('ciao', 'a', {'href': ''})),
            (TextNode("ciao", TextNodeType.LINK, "github.com"),
             LeafNode('ciao', 'a', {'href': 'github.com'})),
        ]

    def test_eq(self):
        for node1, node2 in self.textNodeEqual:
            self.assertEqual(node1, node2)

    def test_unequal(self):
        for node1, node2 in self.textNodeUnequal:
            self.assertNotEqual(node1, node2)

    def test_node_to_html_ok(self):
        for test, case in self.text_to_html:
            self.assertEqual(case, text_node_to_html_node(test))


if __name__ == "__main__":
    unittest.main()
