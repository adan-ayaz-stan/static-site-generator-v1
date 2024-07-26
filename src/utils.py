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
    tmp_nodes = []
    for node in old_nodes:
        text = node.text

        img_nodes = []
        # Extract image nodes
        images = extract_markdown_images(text)
        for image in images:
            # Construct temp string and replace it with a tombstone marker
            tmp_str = text.replace(f"![{image[0]}]({image[1]})", "__image_")
            text = tmp_str

            img_nodes.append(TextNode(image[0], "image", image[1]))

        # Add in the image nodes at the markers
        split_string = text.split("__image_")

        text_nodes = []
        for txt in split_string:
            text_nodes.append(TextNode(txt, "text"))

        # Take first text node - index 0
        # Add the first image after that - index 1
        # Take the second text node - previously index 1, becomes index 2
        # Add the second image after that - index 3
        # Take the third text node - previously index 2, becomes index 4
        # Add the third image after that - index 5
        """
        Order of text nodes: 0, 2, 4, 6, 8, 10
        Order of image nodes: 1, 3, 5, 7, 9, 11
        """

        for i in range(len(img_nodes)):
            tmp_nodes.append(text_nodes[i])
            tmp_nodes.append(img_nodes[i])

            if i == len(img_nodes):
                tmp_nodes.append(text_nodes[i + 1 :])

    return tmp_nodes


# Split nodes link
def split_nodes_link(old_nodes):
    tmp_nodes = []
    for node in old_nodes:
        text = node.text

        img_nodes = []
        # Extract image nodes
        links = extract_markdown_links(text)
        for link in links:
            # Construct temp string and replace it with a tombstone marker
            tmp_str = text.replace(f"[{link[0]}]({link[1]})", "__link_")
            text = tmp_str

            img_nodes.append(TextNode(link[0], "link", link[1]))

        # Add in the image nodes at the markers
        split_string = text.split("__link_")

        text_nodes = []
        for txt in split_string:
            text_nodes.append(TextNode(txt, "text"))

        # Take first text node - index 0
        # Add the first link after that - index 1
        # Take the second text node - previously index 1, becomes index 2
        # Add the second link after that - index 3
        # Take the third text node - previously index 2, becomes index 4
        # Add the third link after that - index 5
        """
        Order of text nodes: 0, 2, 4, 6, 8, 10
        Order of image nodes: 1, 3, 5, 7, 9, 11
        """

        for i in range(len(img_nodes)):
            tmp_nodes.append(text_nodes[i])
            tmp_nodes.append(img_nodes[i])

            if i == len(img_nodes):
                tmp_nodes.append(text_nodes[i + 1 :])

    return tmp_nodes
