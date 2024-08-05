from blocknode import BlockNodeType
import re


_HEADER_PATTERN = re.compile("#{1,6} .+")


def markdown_to_blocks(text: str) -> list[str]:
    nodes = filter(lambda x: x != "", map(
        lambda x: x.strip(), text.split("\n\n")))

    return list(nodes)


def block_to_block_type(block: str) -> BlockNodeType:
    if is_headerblock(block):
        return BlockNodeType.HEADER
    elif is_codeblock(block):
        return BlockNodeType.CODE
    elif is_quoteblock(block):
        return BlockNodeType.QUOTE
    elif is_ulistblock(block):
        return BlockNodeType.ULIST
    elif is_olistblock(block):
        return BlockNodeType.OLIST
    else:
        return BlockNodeType.PARAGRAPH


def is_headerblock(block: str) -> bool:
    return len(block.split("\n")) == 1 and re.match(_HEADER_PATTERN, block)


def is_codeblock(block: str) -> bool:
    return block.startswith("```") and block.endswith("```")


def is_quoteblock(block: str) -> bool:
    lines = block.split("\n")
    return all(map(lambda x: x.startswith(">"), lines))


def is_ulistblock(block: str) -> bool:
    lines = block.split("\n")
    return all(map(lambda x: x.startswith("* ") or x.startswith("- "), lines))


def is_olistblock(block: str) -> bool:
    lines = block.split("\n")
    counter = 1
    for line in lines:
        if not line.startswith(f"{counter}. "):
            return False
        counter += 1
    return True
