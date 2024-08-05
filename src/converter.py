from htmlnode import ParentNode
from block_lexer import markdown_to_blocks, block_to_block_type
from blocknode import BlockNode


def markdown_to_html_node(markdown: str) -> ParentNode:
    html_children = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        block_node = BlockNode(block, block_to_block_type(block))
        html_children.append(block_node.to_html_node())

    return ParentNode('div', html_children)
