from src.textnode import TextNode
from src.utils import split_nodes_delimiter, split_nodes_image, split_nodes_link

"""
Have to apply the delimiter function for bold, italic, code, 
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
