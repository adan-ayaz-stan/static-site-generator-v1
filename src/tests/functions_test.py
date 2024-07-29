import unittest

from src.functions import (
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
    text_to_textnodes,
)
from src.textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"
text_type_link = "link"


class TextToTextNodesTestCase(unittest.TestCase):
    def test_text_seq_1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected_nodes)


class MarkdownToBlockTestCase(unittest.TestCase):
    def test_text_seq_1(self):
        markdown = "# This is a heading\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        # Output should contain blocks seperated by \n\n
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)


class MarkdownToHTMLNodeTestCase(unittest.TestCase):
    def test_text_seq_1(self):
        markdown = "# This is a h1 tag\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        # Output should contain blocks seperated by \n\n
        expected_html = "<div><h1>This is a h1 tag</h1><p>This is a paragraph of text. It has some <strong>bold</strong> and <em>italic</em> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"

        self.assertEqual(markdown_to_html_node(markdown), expected_html)

    def test_text_seq_2(self):
        markdown = "# This is a h1 tag\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"

        expected_html = "<div><h1>This is a h1 tag</h1><p>This is a paragraph of text. It has some <strong>bold</strong> and <em>italic</em> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"

        self.assertEqual(markdown_to_html_node(markdown), expected_html)

    def test_text_seq_3(self):
        markdown = "# This is a h1 tag\n\nThis is a simple paragraph. It has some **bold**, *italic* and `code` blocks inside it.\n\nThe following is an ordered list:\n\n1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item\n\nThe following is an unordered list:\n\n- This is an unordered list\n- This is a list item\n- This is another list item\n\n This is a blockqoute:\n\n> This is the blockquote\n\n This is a code block:\n\n```\nThis is some code\n```\n"

        expected_html = "<div><h1>This is a h1 tag</h1><p>This is a simple paragraph. It has some <strong>bold</strong>, <em>italic</em> and <code>code</code> blocks inside it.</p><p>The following is an ordered list:</p><ol><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ol><p>The following is an unordered list:</p><ul><li>This is an unordered list</li><li>This is a list item</li><li>This is another list item</li></ul><p>This is a blockqoute:</p><blockquote>This is the blockquote</blockquote><p>This is a code block:</p><code>This is some code</code></div>"

        self.assertEqual(markdown_to_html_node(markdown), expected_html)


class ExtractTitleTestCase(unittest.TestCase):
    def test_simple_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_title_with_whitespace(self):
        markdown = "#   Hello   "
        self.assertEqual(extract_title(markdown), "Hello")

    def test_multiple_lines(self):
        markdown = "This is a regular line\n# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_no_title(self):
        markdown = "This is a regular line\nThis is another line"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_title(self):
        markdown = "#"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_multiple_titles(self):
        markdown = "# First title\n# Second title"
        self.assertEqual(extract_title(markdown), "First title")
