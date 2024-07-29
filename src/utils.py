import re

from textnode import TextNode

"""
Input:
node = TextNode("This is text with a `code block` word", text_type_text)
new_nodes = split_nodes_delimiter([node], "`", text_type_code)

Output:
new_nodes = [
    TextNode("This is text with a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" word", text_type_text),
]
"""


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes in a list of nodes based on a delimiter and text type.

    Args:
        old_nodes (list): List of nodes to process.
        delimiter (str): Delimiter to split text nodes on.
        text_type (str): Text type to assign to new nodes.

    Returns:
        list: New list of nodes with text nodes split based on delimiter.
    """
    new_nodes = []
    temp_text = ""
    for node in old_nodes:
        if node.text_type == "text":
            temp_text += node.text
        else:
            if temp_text:
                # Split text node into multiple nodes based on delimiter
                text_parts = temp_text.split(delimiter)
                for i, part in enumerate(text_parts):
                    if i % 2 == 0:
                        # Even parts are regular text
                        new_nodes.append(TextNode(part, "text"))
                    else:
                        # Odd parts are code/bold/italic text
                        new_nodes.append(TextNode(part, text_type))
                temp_text = ""
            new_nodes.append(node)
    if temp_text:
        # Split text node into multiple nodes based on delimiter
        text_parts = temp_text.split(delimiter)
        for i, part in enumerate(text_parts):
            if i % 2 == 0:
                # Even parts are regular text
                new_nodes.append(TextNode(part, "text"))
            else:
                # Odd parts are code/bold/italic text
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


# Create a function extract_markdown_images(text) that takes raw markdown text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.


def extract_markdown_images(text):
    s = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return s


# Create a function extract_markdown_links(text) that takes raw markdown text and returns a list of tuples. Each tuple should contain the link text and the URL of any markdown links.


def extract_markdown_links(text):
    s = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return s


# Split nodes image
def split_nodes_image(old_nodes):
    """
    Split nodes into text and image nodes.

    Args:
        old_nodes (list): List of nodes to be split.

    Returns:
        list: List of split nodes.
    """
    new_nodes = []
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        remaining_text = text
        last_index = 0
        for image in images:
            image_tag = f"![{image[0]}]({image[1]})"
            index = remaining_text.find(image_tag)
            if index != -1:
                new_nodes.append(TextNode(remaining_text[last_index:index], "text"))
                new_nodes.append(TextNode(image[0], "image", image[1]))
                last_index = index + len(image_tag)

        # Add the remaining text after the last image, only if it's not empty
        remaining_text_after_last_image = remaining_text[last_index:]
        if remaining_text_after_last_image.strip():
            new_nodes.append(TextNode(remaining_text_after_last_image, "text"))

    return new_nodes


# Split nodes link
def split_nodes_link(old_nodes):
    """
    Split nodes into text and link nodes.

    Args:
        old_nodes (list): List of nodes to be split.

    Returns:
        list: List of split nodes.
    """

    tmp_nodes = []
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)

        if not links:
            tmp_nodes.append(node)
            continue

        remaining_text = text
        last_index = 0
        for link in links:
            link_tag = f"[{link[0]}]({link[1]})"
            index = remaining_text.find(link_tag)
            if index != -1:
                tmp_nodes.append(TextNode(remaining_text[last_index:index], "text"))
                tmp_nodes.append(TextNode(link[0], "link", link[1]))
                last_index = index + len(link_tag)

        # Add the remaining text after the last link, only if it's not empty
        remaining_text_after_last_link = remaining_text[last_index:]
        if remaining_text_after_last_link.strip():
            tmp_nodes.append(TextNode(remaining_text_after_last_link, "text"))

    return tmp_nodes


def block_to_block_type(block):

    # Heading
    split_string_h_check = block.split(" ", 1)
    hash_chars = 0
    for i in range(len(split_string_h_check[0])):
        if split_string_h_check[0][i] == "#":
            hash_chars += 1

    if hash_chars == len(split_string_h_check[0]):
        # trim the rest of the string and also return it

        return (f"h{hash_chars}", split_string_h_check[1].strip())

    # Ordered List
    pattern = r"^\d+\..*$"
    list_items = re.findall(pattern, block, re.MULTILINE)
    if list_items:
        # Remove the number from the list items
        list_items = [item[2:].strip() for item in list_items]
        return ("ol", list_items)

    # Unordered list block
    pattern = r"^[\*-].*$"
    list_items = re.findall(pattern, block, re.MULTILINE)
    if list_items:
        # Remove * or - from the list items
        list_items = [
            item[1:].strip() if item[0] in ["*", "-"] else item for item in list_items
        ]
        return ("ul", list_items)

    # Blockqoute Block
    if block[:1] == ">":
        return ("blockquote", block[1:].strip())

    # Code Block
    if (block[:3] == "```" and block[-3:] == "```") or (
        block[:3] == "~~~" and block[-3:] == "~~~"
    ):
        return ("code", block[3:-3].strip())

    # Normal Paragraph
    return ("p", block.strip())
