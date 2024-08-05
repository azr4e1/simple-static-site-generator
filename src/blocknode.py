from typing import Any
from textnode import TextNodeType, TextNode
from htmlnode import ParentNode
from enum import Enum, auto
from inline_lexer import text_to_textnodes
from functools import reduce


class BlockNodeType(Enum):
    HEADER = auto()
    CODE = auto()
    QUOTE = auto()
    ULIST = auto()
    OLIST = auto()
    PARAGRAPH = auto()


class BlockNode:
    def __init__(self, text: str,
                 text_type: TextNodeType) -> None:
        self.text = text
        self.text_type = text_type

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BlockNode):
            return False
        return (self.text == other.text
                and self.text_type == other.text_type)

    def __repr__(self) -> str:
        return f"BlockNode({self.text}, {self.text_type})"

    def to_html_node(self) -> ParentNode:
        match self.text_type:
            case BlockNodeType.PARAGRAPH:
                return paragraph_to_html(self.text)
            case BlockNodeType.HEADER:
                return header_to_html(self.text)
            case BlockNodeType.CODE:
                return code_to_html(self.text)
            case BlockNodeType.QUOTE:
                return quote_to_html(self.text)
            case BlockNodeType.ULIST:
                return ulist_to_html(self.text)
            case BlockNodeType.OLIST:
                return olist_to_html(self.text)
            case _:
                raise ValueError(
                    f"text type {self.text_type} not recognized; text:\n{self.text}")


def paragraph_to_html(text: str) -> ParentNode:
    md_children = reduce(
        lambda x, y: x + text_to_textnodes(y), text.split("\n"), [])
    html_children = list(map(lambda x: x.to_html_node(), md_children))
    return ParentNode('p', html_children)


def code_to_html(text: str) -> ParentNode:
    html_children = [TextNode(text.removeprefix('```').removesuffix(
        '```'), TextNodeType.TEXT).to_html_node()]
    return ParentNode('pre', [ParentNode('code', html_children)])


def header_to_html(text: str) -> ParentNode:
    counter = 0
    prefix = "#"
    while True:
        if text.startswith(prefix):
            text = text.removeprefix(prefix)
            counter += 1
        else:
            break
    text = text.lstrip()
    md_children = text_to_textnodes(text)
    html_children = list(map(lambda x: x.to_html_node(), md_children))

    return ParentNode(f"h{counter}", html_children)


def quote_to_html(text: str) -> ParentNode:
    lines = text.split("\n")
    prefix = ">"
    clean_text = "\n".join(list(map(lambda x: x.removeprefix(prefix), lines)))
    md_children = text_to_textnodes(clean_text)
    html_children = list(map(lambda x: x.to_html_node(), md_children))

    return ParentNode("blockquote", html_children)


def ulist_to_html(text: str) -> ParentNode:
    html_children = []
    lines = text.split("\n")
    for line in lines:
        # '* ' or '- ' have length 2
        line_content = line[2:]
        line_md_children = text_to_textnodes(line_content)
        line_html_children = list(
            map(lambda x: x.to_html_node(), line_md_children))
        html_children.append(ParentNode('li', line_html_children))

    return ParentNode('ul', html_children)


def olist_to_html(text: str) -> ParentNode:
    html_children = []
    lines = text.split("\n")
    for num in range(len(lines)):
        line = lines[num]
        index = num+1
        line_content = line.removeprefix(f"{index}. ")
        line_md_children = text_to_textnodes(line_content)
        line_html_children = list(
            map(lambda x: x.to_html_node(), line_md_children))
        html_children.append(ParentNode('li', line_html_children))

    return ParentNode('ol', html_children)
