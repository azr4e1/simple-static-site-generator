import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
import logging


logging.basicConfig(filename='test.txt')


class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.htmlNodeCase = [
            (HTMLNode("ciao", "a",  None, {'href': 'prova'}), ' href="prova"'),
            (HTMLNode("ciao", "a",  None, {
             'href': 'https://github.com', 'target': '_blank'}), ' href="https://github.com" target="_blank"'),
            (HTMLNode("ok", "p", None, {'meta': 'static'}), ' meta="static"'),
        ]
        self.leafNodeCaseCorrect = [
            (LeafNode("ok", "a", {'href': 'github.com'}),
             '<a href="github.com">ok</a>'),
            (LeafNode("ciao", "p"), '<p>ciao</p>'),
            (LeafNode("ok"), 'ok'),
            (LeafNode("ok", None, {'href': 'github.com'}), 'ok'),
        ]
        self.leafNodeCaseError = [
            LeafNode(None, "a", None),
            LeafNode(None, "a", {'href': 'github.com'}),
            LeafNode(None, None, {'href': 'github.com'}),
        ]
        self.parentNodeCaseCorrect = [
            (ParentNode(
                "p",
                [
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                ],
            ), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"),
            (ParentNode(
                "p",
                [
                    ParentNode(
                        'div',
                        [
                            LeafNode("Bold text", "b"),
                            LeafNode("Normal text", None),
                        ],
                        props={'color': 'red'},
                    ),
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                ],
            ), '<p><div color="red"><b>Bold text</b>Normal text</div><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'),
            (ParentNode(
                "p",
                [
                    ParentNode(
                        'div',
                        [
                            ParentNode(
                                'div',
                                [
                                    LeafNode("Very inner text", 'b',
                                             props={'haha': 'ok'}),
                                ],
                                props={'color': 'blue'},
                            ),
                            LeafNode("Bold text", "b"),
                            LeafNode("Normal text", None),
                        ],
                        props={'color': 'red'},
                    ),
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                ],
            ), '<p><div color="red"><div color="blue"><b haha="ok">Very inner text</b></div><b>Bold text</b>Normal text</div><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'),
            (
                ParentNode(
                    'p',
                    [
                        ParentNode(
                            "p",
                            [
                                ParentNode(
                                    'p',
                                    [
                                        LeafNode("Normal text", None,
                                                 props={'haha': 'ok'}),
                                    ]
                                )
                            ],
                            props={'ok': 'haha'},
                        )
                    ]
                ), '<p><p ok="haha"><p>Normal text</p></p></p>'),
        ]
        self.parentNodeCaseError = [
            (ParentNode(
                None,
                [
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                ],
            ), ValueError, "parent node needs a tag"),
            (ParentNode(
                "p",
                [
                    ParentNode(
                        'div',
                        [
                            LeafNode(None, 'b'),
                            LeafNode("Normal text", None),
                        ],
                        props={'color': 'red'},
                    ),
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                ],
            ), ValueError, "leaf node nees a value"),
            (ParentNode(
                "p",
                [
                    ParentNode(
                        'div',
                        [
                            ParentNode(
                                'div',
                                [
                                ],
                                props={'color': 'blue'},
                            ),
                            LeafNode("Bold text", "b"),
                            LeafNode("Normal text", None),
                        ],
                        props={'color': 'red'},
                    ),
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                ],
            ), ValueError, "parent node needs children nodes"),
            (
                ParentNode(
                    'p',
                    None
                ), ValueError, "parent node needs children nodes"),
        ]

    def test_props_to_html(self):
        for test, case in self.htmlNodeCase:
            string = test.props_to_html()
            self.assertEqual(string, case)

    def test_to_html_ok(self):
        for test, case in self.leafNodeCaseCorrect:
            string = test.to_html()
            self.assertEqual(string, case)

    def test_to_html_error(self):
        for test in self.leafNodeCaseError:
            self.assertRaises(ValueError, test.to_html)

    def test_parent_node_ok(self):
        for test, case in self.parentNodeCaseCorrect:
            string = test.to_html()
            self.assertEqual(string, case)

    def test_parent_node_error(self):
        for test, exception, msg in self.parentNodeCaseError:
            with self.assertRaises(exception) as m:
                test.to_html()
            self.assertEqual(msg, m.exception.args[0])


if __name__ == "__main__":
    unittest.main()
