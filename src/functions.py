from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode
from src.utils import (
    block_to_block_type,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)

"""
Have to apply the delimiter function for bold, italic, code, 

There seems to be an order to how to apply the delimiter functions incase of similar delimiters as ** and *. In such case, we must apply the larger delimiter first (**). Then the smaller delimiter.

TODO: Find a solution to the delimiter hierarchy problem.
"""


def text_to_textnodes(markdown_text):
    node = TextNode(markdown_text, "text")

    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([node], "`", "code"), "**", "bold"
                ),
                "*",
                "italic",
            )
        )
    )


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    # Remove any empty blocks
    split_blocks = [block for block in split_blocks if block != ""]
    # Remove whitespace from the beginning and end of each block
    return [block.strip() for block in split_blocks]


# MARKDOWN TO HTML NODE
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    """
    Loop over each block:
    
    Determine the type of block (you already have a function for this)
    
    Based on the type of block, create a new HTMLNode with the proper data
    
    Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline  markdown using previously created functions (think TextNode -> HTMLNode).
    """
    root_children = []

    for block in blocks:
        # Determine the block type
        block_type = block_to_block_type(block)

        # Create a new HTML Node based on that type which will most likely be a parent node
        children_nodes = text_to_textnodes(block)
        parent_node = ParentNode(
            children=children_nodes, tag=block_type, value=None, props=None
        )

        root_children.append(parent_node)

    return ParentNode(
        children=root_children, tag="div", value=None, props=None
    ).to_html()
