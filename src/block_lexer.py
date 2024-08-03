from textnode import TextNode, TextNodeType


def markdown_to_blocks(text: str) -> list[str]:
    nodes = filter(lambda x: x != "", map(
        lambda x: x.strip(), text.split("\n\n")))

    return list(nodes)
