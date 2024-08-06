from textnode import TextNode, TextNodeType
import re


_IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\((.*?)\)")
_LINK_PATTERN = re.compile(r"\[(.*?)\]\((.*?)\)")
_DEFAULT_DELIMITERS = {
    TextNodeType.CODE: '`',
    TextNodeType.BOLD: '**',
    TextNodeType.ITALIC: '*',
}
DELIMITERS = _DEFAULT_DELIMITERS.copy()


def split_nodes_delimiter(old_nodes: list[TextNode],
                          delimiter: str,
                          text_type: TextNodeType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # don't split non text nodes
        if node.text_type != TextNodeType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        # if number of split is even, it means delimiter wasn't closed
        if len(split_text) % 2 == 0:
            raise ValueError(
                f"invalid markdown syntax ('{delimiter}' not closed)")

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextNodeType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # don't split non text nodes
        if node.text_type != TextNodeType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        text = node.text
        for image in images:
            delimiter = f"![{image[0]}]({image[1]})"
            split_text = text.split(delimiter, maxsplit=1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextNodeType.TEXT))
            new_nodes.append(
                TextNode(image[0], TextNodeType.IMAGE, url=image[1]))
            text = split_text[1]
        if text != "":
            new_nodes.append(TextNode(text, TextNodeType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # don't split non text nodes
        if node.text_type != TextNodeType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        text = node.text
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            split_text = text.split(delimiter, maxsplit=1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextNodeType.TEXT))
            new_nodes.append(
                TextNode(link[0], TextNodeType.LINK, url=link[1]))
            text = split_text[1]
        if text != "":
            new_nodes.append(TextNode(text, TextNodeType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextNodeType.TEXT)]
    nodes = split_nodes_link(split_nodes_image(nodes))
    # enums are ordered.
    for text_type in TextNodeType:
        match text_type:
            case TextNodeType.IMAGE | TextNodeType.LINK | TextNodeType.TEXT:
                continue
            case _:
                if text_type not in DELIMITERS:
                    raise ValueError(f"no delimiters defined for {text_type}")
                delimiter = DELIMITERS[text_type]
                nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    return nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(_IMAGE_PATTERN, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(_LINK_PATTERN, text)
