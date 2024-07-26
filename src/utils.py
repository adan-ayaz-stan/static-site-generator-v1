import re

from src.textnode import TextNode

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
    tmp_nodes = []
    for node in old_nodes:
        text = node.text
        if delimiter in text:
            split_txt = text.split(delimiter)

            for i in range(len(split_txt)):
                if i == 0:
                    tmp_nodes.append(TextNode(split_txt[i], "text"))
                elif i == len(split_txt) - 1:
                    tmp_nodes.append(TextNode(split_txt[i], "text"))
                else:
                    if i % 2 == 0:
                        tmp_nodes.append(TextNode(split_txt[i], "text"))
                    else:
                        tmp_nodes.append(TextNode(split_txt[i], text_type))
        else:
            tmp_nodes.append(node)
    return tmp_nodes


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