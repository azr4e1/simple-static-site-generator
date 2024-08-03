from inline_lexer import (split_nodes_delimiter,
                          extract_markdown_links,
                          extract_markdown_images,
                          split_nodes_link,
                          split_nodes_image,
                          text_to_textnodes)
import unittest
from textnode import TextNode, TextNodeType


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexerTestOk = [
            ([TextNode("This is text with a `code block` word", TextNodeType.TEXT)],
             '`',
             TextNodeType.CODE,
             [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode(" word", TextNodeType.TEXT),
            ]),
            ([TextNode("This is `text` with a `code block` word", TextNodeType.TEXT)],
             '`',
             TextNodeType.CODE,
             [
                TextNode("This is ", TextNodeType.TEXT),
                TextNode("text", TextNodeType.CODE),
                TextNode(" with a ", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode(" word", TextNodeType.TEXT),
            ]),
            ([TextNode("This is text with a *italic block* word", TextNodeType.TEXT)],
             '*',
             TextNodeType.ITALIC,
             [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("italic block", TextNodeType.ITALIC),
                TextNode(" word", TextNodeType.TEXT),
            ]),
            ([TextNode("This is text with a **bold block** word", TextNodeType.TEXT)],
             '**',
             TextNodeType.BOLD,
             [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bold block", TextNodeType.BOLD),
                TextNode(" word", TextNodeType.TEXT),
            ]),
            ([TextNode("This is text with a `code block` word", TextNodeType.TEXT),
              TextNode("`code block`", TextNodeType.TEXT),
              TextNode("**bold**", TextNodeType.BOLD)],
             '`',
             TextNodeType.CODE,
             [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode(" word", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode("**bold**", TextNodeType.BOLD),
            ]),
            ([TextNode("This is text with a `code block` word", TextNodeType.TEXT),
              TextNode("`code block`", TextNodeType.CODE),
              TextNode("**bold** text", TextNodeType.TEXT)],
             '`',
             TextNodeType.CODE,
             [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode(" word", TextNodeType.TEXT),
                TextNode("`code block`", TextNodeType.CODE),
                TextNode("**bold** text", TextNodeType.TEXT),
            ]),
            ([TextNode("This is *text* with a `code block` word", TextNodeType.TEXT)],
             '`',
             TextNodeType.CODE,
             [
                TextNode("This is *text* with a ", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode(" word", TextNodeType.TEXT),
            ]),
            ([TextNode("This is *text* with a `code block` word", TextNodeType.TEXT)],
             '*',
             TextNodeType.ITALIC,
             [
                TextNode("This is ", TextNodeType.TEXT),
                TextNode("text", TextNodeType.ITALIC),
                TextNode(" with a `code block` word", TextNodeType.TEXT),
            ]),
            ([TextNode("This is text with a `code block` word", TextNodeType.CODE)],
             '`',
             TextNodeType.CODE,
             [
                TextNode("This is text with a `code block` word",
                         TextNodeType.CODE)
            ]),
            ([TextNode("This is *text* with a `code block` word", TextNodeType.TEXT)],
             '**',
             TextNodeType.BOLD,
             [
                TextNode("This is *text* with a `code block` word",
                         TextNodeType.TEXT)
            ]),
            ([TextNode("This is **text****ciao** with a `code block` word", TextNodeType.TEXT)],
             '**',
             TextNodeType.BOLD,
             [
                TextNode("This is ", TextNodeType.TEXT),
                TextNode("text", TextNodeType.BOLD),
                TextNode("ciao", TextNodeType.BOLD),
                TextNode(" with a `code block` word", TextNodeType.TEXT)
            ]),
        ]
        self.lexerTestError = [
            ([TextNode("This is *text* with a code block` word", TextNodeType.TEXT)],
             '`',
             TextNodeType.CODE,
             ValueError,
             "invalid markdown syntax ('`' not closed)"
             ),
            ([TextNode("This is *text with a code block` word", TextNodeType.TEXT)],
             '*',
             TextNodeType.ITALIC,
             ValueError,
             "invalid markdown syntax ('*' not closed)"
             ),
            ([TextNode("This is *text** with a code block` word", TextNodeType.TEXT)],
             '**',
             TextNodeType.BOLD,
             ValueError,
             "invalid markdown syntax ('**' not closed)"
             ),
            ([TextNode("This is *text* with a `code block` word", TextNodeType.TEXT),
              TextNode("This is *text* with a code block` word", TextNodeType.TEXT)],
             '`',
             TextNodeType.CODE,
             ValueError,
             "invalid markdown syntax ('`' not closed)"
             ),
        ]
        self.imageExtractor = [
            (
                "ciao ![come](stai?) tutto bene",
                [("come", "stai?")]
            ),
            (
                "ciao ![come](stai?) ![tutto](bene)",
                [("come", "stai?"), ("tutto", "bene")]
            ),
            (
                "ciao ![come](stai?) [tutto](bene)",
                [("come", "stai?")]
            ),
            (
                "",
                []
            ),
            (
                "ciao ![come](stai? tutto bene",
                []
            ),
            (
                "ciao ![come(stai?) tutto bene",
                []
            ),
            ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
             [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
             )
        ]
        self.linkExtractor = [
            (
                "ciao ![come](stai?) tutto bene",
                []
            ),
            (
                "ciao [come](stai?) ![tutto](bene)",
                [("come", "stai?")]
            ),
            (
                "ciao [come](stai?) [tutto](bene)",
                [("come", "stai?"), ("tutto", "bene")]
            ),
            (
                "",
                []
            ),
            (
                "ciao [come](stai? tutto bene",
                []
            ),
            (
                "ciao [come(stai?) tutto bene",
                []
            ),
            (
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                [("to boot dev", "https://www.boot.dev"),
                 ("to youtube", "https://www.youtube.com/@bootdotdev")]
            )
        ]
        self.linkSplitTest = [
            (
                [TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode("This is text with a link ", TextNodeType.TEXT),
                    TextNode("to boot dev", TextNodeType.LINK,
                             "https://www.boot.dev"),
                    TextNode(" and ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode("This is text with a link ", TextNodeType.TEXT),
                    TextNode("to boot dev", TextNodeType.LINK,
                             "https://www.boot.dev"),
                    TextNode(
                        " and ![to youtube](https://www.youtube.com/@bootdotdev)", TextNodeType.TEXT),
                ]),
            (
                [TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) ", TextNodeType.TEXT),
                 TextNode(
                     "and [to youtube](https://www.youtube.com/@bootdotdev)", TextNodeType.TEXT)
                 ],
                [
                    TextNode("This is text with a link ", TextNodeType.TEXT),
                    TextNode("to boot dev", TextNodeType.LINK,
                             "https://www.boot.dev"),
                    TextNode(" ", TextNodeType.TEXT),
                    TextNode("and ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link [to boot dev]https://www.boot.dev) ", TextNodeType.TEXT),
                 TextNode(
                     "and [to youtube](https://www.youtube.com/@bootdotdev)", TextNodeType.TEXT)
                 ],
                [
                    TextNode(
                        "This is text with a link [to boot dev]https://www.boot.dev) ", TextNodeType.TEXT),
                    TextNode(
                        "and ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link [to boot dev]https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode(
                        "This is text with a link ", TextNodeType.TEXT),
                    TextNode(
                        "to boot dev]https://www.boot.dev) and [to youtube", TextNodeType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link [](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode(
                        "This is text with a link ", TextNodeType.TEXT),
                    TextNode(
                        "", TextNodeType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link [to youtube]()",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode(
                        "This is text with a link ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.LINK, ""
                    ),
                ]),
        ]
        self.imageSplitTest = [
            (
                [TextNode(
                    "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode("This is text with a link ", TextNodeType.TEXT),
                    TextNode("to boot dev", TextNodeType.IMAGE,
                             "https://www.boot.dev"),
                    TextNode(
                        " and [to youtube](https://www.youtube.com/@bootdotdev)", TextNodeType.TEXT)
                ]),
            (
                [TextNode(
                    "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode("This is text with a link ", TextNodeType.TEXT),
                    TextNode("to boot dev", TextNodeType.IMAGE,
                             "https://www.boot.dev"),
                    TextNode(" and ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.IMAGE, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link ![to boot dev](https://www.boot.dev) ", TextNodeType.TEXT),
                 TextNode(
                     "and ![to youtube](https://www.youtube.com/@bootdotdev)", TextNodeType.TEXT)
                 ],
                [
                    TextNode("This is text with a link ", TextNodeType.TEXT),
                    TextNode("to boot dev", TextNodeType.IMAGE,
                             "https://www.boot.dev"),
                    TextNode(" ", TextNodeType.TEXT),
                    TextNode("and ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.IMAGE, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link [to boot dev]https://www.boot.dev) ", TextNodeType.TEXT),
                 TextNode(
                     "and ![to youtube](https://www.youtube.com/@bootdotdev)", TextNodeType.TEXT)
                 ],
                [
                    TextNode(
                        "This is text with a link [to boot dev]https://www.boot.dev) ", TextNodeType.TEXT),
                    TextNode("and ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.IMAGE, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link ![to boot dev]https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode(
                        "This is text with a link ", TextNodeType.TEXT),
                    TextNode(
                        "to boot dev]https://www.boot.dev) and ![to youtube", TextNodeType.IMAGE, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link ![](https://www.youtube.com/@bootdotdev)",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode(
                        "This is text with a link ", TextNodeType.TEXT),
                    TextNode(
                        "", TextNodeType.IMAGE, "https://www.youtube.com/@bootdotdev"
                    ),
                ]),
            (
                [TextNode(
                    "This is text with a link ![to youtube]()",
                    TextNodeType.TEXT,
                )],
                [
                    TextNode(
                        "This is text with a link ", TextNodeType.TEXT),
                    TextNode(
                        "to youtube", TextNodeType.IMAGE, ""
                    ),
                ]),
        ]

        self.text_to_textnode_test_ok = [
            ("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
             [
                 TextNode("This is ", TextNodeType.TEXT),
                 TextNode("text", TextNodeType.BOLD),
                 TextNode(" with an ", TextNodeType.TEXT),
                 TextNode("italic", TextNodeType.ITALIC),
                 TextNode(" word and a ", TextNodeType.TEXT),
                 TextNode("code block", TextNodeType.CODE),
                 TextNode(" and an ", TextNodeType.TEXT),
                 TextNode("obi wan image", TextNodeType.IMAGE,
                          "https://i.imgur.com/fJRm4Vk.jpeg"),
                 TextNode(" and a ", TextNodeType.TEXT),
                 TextNode("link", TextNodeType.LINK, "https://boot.dev"),
             ]),
            ("This is **text****italic** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
             [
                 TextNode("This is ", TextNodeType.TEXT),
                 TextNode("text", TextNodeType.BOLD),
                 TextNode("italic", TextNodeType.BOLD),
                 TextNode(" word and a ", TextNodeType.TEXT),
                 TextNode("code block", TextNodeType.CODE),
                 TextNode(" and an ", TextNodeType.TEXT),
                 TextNode("obi wan image", TextNodeType.IMAGE,
                          "https://i.imgur.com/fJRm4Vk.jpeg"),
                 TextNode(" and a ", TextNodeType.TEXT),
                 TextNode("link", TextNodeType.LINK, "https://boot.dev"),
             ]),
            ("This is **text****italic** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)",
             [
                 TextNode("This is ", TextNodeType.TEXT),
                 TextNode("text", TextNodeType.BOLD),
                 TextNode("italic", TextNodeType.BOLD),
                 TextNode(" word and a ", TextNodeType.TEXT),
                 TextNode("code block", TextNodeType.CODE),
                 TextNode(" and an ", TextNodeType.TEXT),
                 TextNode("obi wan image", TextNodeType.IMAGE,
                          "https://i.imgur.com/fJRm4Vk.jpeg"),
                 TextNode(" and a ", TextNodeType.TEXT),
                 TextNode("obi wan image", TextNodeType.LINK,
                          "https://i.imgur.com/fJRm4Vk.jpeg"),
             ]),
            ("This is **text****italic** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [obi wan image(https://i.imgur.com/fJRm4Vk.jpeg)",
             [
                 TextNode("This is ", TextNodeType.TEXT),
                 TextNode("text", TextNodeType.BOLD),
                 TextNode("italic", TextNodeType.BOLD),
                 TextNode(" word and a ", TextNodeType.TEXT),
                 TextNode("code block", TextNodeType.CODE),
                 TextNode(" and an ", TextNodeType.TEXT),
                 TextNode("obi wan image", TextNodeType.IMAGE,
                          "https://i.imgur.com/fJRm4Vk.jpeg"),
                 TextNode(
                     " and a [obi wan image(https://i.imgur.com/fJRm4Vk.jpeg)", TextNodeType.TEXT),
             ]),
        ]
        self.text_to_textnode_test_error = [
            ("This is **text* with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
             ValueError, "invalid markdown syntax ('**' not closed)"
             ),
            ("This is **text****italic** word and a code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
             ValueError, "invalid markdown syntax ('`' not closed)"
             ),
            ("This is **text** *italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)",
             ValueError, "invalid markdown syntax ('*' not closed)")
        ]

    def test_lexer_correctly_splits_nodes(self):
        for nodes, delim, node_type, case in self.lexerTestOk:
            result = split_nodes_delimiter(nodes, delim, node_type)
            self.assertEqual(case, result)

    def test_lexer_error(self):
        for nodes, delim, node_type, exception, msg in self.lexerTestError:
            with self.assertRaises(exception) as m:
                split_nodes_delimiter(nodes, delim, node_type)
            self.assertEqual(msg, m.exception.args[0])

    def test_image_extractor(self):
        for test, case in self.imageExtractor:
            result = extract_markdown_images(test)
            self.assertListEqual(result, case)

    def test_link_extractor(self):
        for test, case in self.linkExtractor:
            result = extract_markdown_links(test)
            self.assertListEqual(result, case)

    def test_image_split(self):
        for test, case in self.imageSplitTest:
            result = split_nodes_image(test)
            self.assertListEqual(result, case)

    def test_link_split(self):
        for test, case in self.linkSplitTest:
            result = split_nodes_link(test)
            self.assertListEqual(result, case)

    def test_text_to_textnode(self):
        for test, case in self.text_to_textnode_test_ok:
            result = text_to_textnodes(test)
            self.assertListEqual(result, case)

    def test_text_to_textnode_error(self):
        for test, exception, msg in self.text_to_textnode_test_error:
            with self.assertRaises(exception) as m:
                text_to_textnodes(test)
            self.assertEqual(msg, m.exception.args[0])


if __name__ == "__main__":
    unittest.main()
