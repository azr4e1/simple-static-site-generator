from __future__ import annotations
from typing import Optional, Any, Sequence
from functools import reduce


class HTMLNode:
    def __init__(self,
                 value: Optional[str] = None,
                 tag: Optional[str] = None,
                 children: Optional[Sequence[HTMLNode]] = None,
                 props: Optional[dict[str, str]] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        string = reduce(lambda x, y: x +
                        f' {y[0]}="{y[1]}"', self.props.items(), "")
        return string

    def __eq__(self, o: Any):
        if not isinstance(o, HTMLNode):
            return False

        return (self.value == o.value
                and self.tag == o.tag
                and self.children == o.children
                and self.props == o.props)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 children: Sequence[HTMLNode],
                 props: Optional[dict[str, str]] = None) -> None:
        super().__init__(None, tag, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("parent node needs a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("parent node needs children nodes")

        children_string = reduce(
            lambda x, y: x + y.to_html(), self.children, "")
        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self,
                 value: str,
                 tag: Optional[str] = None,
                 props: Optional[dict[str, str]] = None) -> None:
        super().__init__(value, tag, None, props)

    def to_html(self) -> str:
        if self.tag == 'img':
            return f"<{self.tag}{self.props_to_html()}>"
        if self.value is None or self.value == '':
            raise ValueError("leaf node nees a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
