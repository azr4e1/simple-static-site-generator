from __future__ import annotations
from typing import Optional, Any
from htmlnode import LeafNode
from enum import Enum, auto


class TextNodeType(Enum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    IMAGE = auto()
    LINK = auto()


class TextNode:
    def __init__(self, text: str,
                 text_type: TextNodeType,
                 url: Optional[str] = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextNodeType.TEXT:
            return LeafNode(text_node.text)
        case TextNodeType.BOLD:
            return LeafNode(text_node.text, 'b')
        case TextNodeType.ITALIC:
            return LeafNode(text_node.text, 'i')
        case TextNodeType.CODE:
            return LeafNode(text_node.text, 'code')
        case TextNodeType.LINK:
            return LeafNode(text_node.text, 'a', {'href': text_node.url
                                                  if text_node.url is not None
                                                  else ""})
        case TextNodeType.IMAGE:
            return LeafNode(text_node.text, 'img', {'alt': text_node.text,
                                                    'src': text_node.url
                                                    if text_node.url is not None
                                                    else ""})
        case _:
            raise ValueError("text type not supported")
