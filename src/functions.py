from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode
from utils import (
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
        (block_type, block_text) = block_to_block_type(block)

        if block_type == "ul" or block_type == "ol":
            li_nodes = []

            # Block text is a list of items
            for text in block_text:
                # Create a new HTML Node based on that type which will most likely be a parent node
                children_nodes = text_to_textnodes(text)
                li_node = ParentNode(
                    children=children_nodes, tag="li", value=None, props=None
                )
                li_nodes.append(li_node)

            parent_node = ParentNode(
                children=li_nodes, tag=block_type, value=None, props=None
            )
            root_children.append(parent_node)
            continue

        if block_type == "code":
            child_node = text_to_textnodes(block_text)
            sub_parent_node = ParentNode(children=child_node, tag="code")
            parent_node = ParentNode(children=[sub_parent_node], tag="pre")
            root_children.append(parent_node)
            continue

        # Create a new HTML Node based on that type which will most likely be a parent node
        children_nodes = text_to_textnodes(block_text)
        parent_node = ParentNode(
            children=children_nodes, tag=block_type, value=None, props=None
        )

        root_children.append(parent_node)

    return ParentNode(
        children=root_children, tag="div", value=None, props=None
    ).to_html()


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.lstrip().startswith("#"):
            title = line[1:].strip()  # remove the # and any leading/trailing whitespace
            if title:  # make sure the title is not empty
                return title
    raise ValueError("No H1 header found in the markdown")


def read_file(filename):
    try:
        with open(filename, "r") as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        print(f"Sorry, the file {filename} does not exist.")
        return None


def write_to_file(filename, contents):
    try:
        with open(filename, "w") as file:
            file.write(contents)
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file from path
    md_file = read_file(from_path)
    template_file = read_file(template_path)

    html_from_md = markdown_to_html_node(md_file)

    title = extract_title(md_file)

    print("Generated page title: ", title)

    file_with_title = template_file.replace("{{ Title }}", title)
    file_with_content = file_with_title.replace("{{ Content }}", html_from_md)

    write_to_file(dest_path, file_with_content)
