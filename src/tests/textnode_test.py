import unittest

from src.textnode import TextNode
from src.utils import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_equality(self):
        node_1 = TextNode("Hello World", "link", "https://www.google.com")
        node_2 = TextNode("Hello World", "link", "https://www.google.com")

        self.assertEqual(node_1, node_2)

    def test_non_equality(self):
        node_1 = TextNode("Hello World", "image", "https://www.google.com")
        node_2 = TextNode("Hello World", "link", "https://www.google.com")

        self.assertNotEqual(node_1, node_2)

    def test_repr(self):
        node_1 = TextNode("Hello World", "code", "https://www.google.com")

        self.assertEqual(
            node_1.__repr__(), "TextNode(Hello World, code, https://www.google.com)"
        )

    def test_to_html_text(self):
        node_text = TextNode("Hello World", "text")
        self.assertEqual(node_text.to_html(), "Hello World")

    def test_to_html_bold(self):
        node_bold = TextNode("Bold Text", "bold")
        self.assertEqual(node_bold.to_html(), "<b>Bold Text</b>")

    def test_to_html_link(self):
        node_link = TextNode("Click here", "link", "https://www.example.com")
        self.assertEqual(
            node_link.to_html(),
            "<a href='https://www.example.com'>Click here</a>",
        )

    def test_unsupported_text_type(self):
        with self.assertRaises(Exception):
            node_1 = TextNode("Hello World", "unsupported", "https://www.google.com")

    def test_link_node_with_none_url(self):
        node_link = TextNode("Click here", "link", None)
        self.assertEqual(
            node_link.to_html(), "<a href='#'>Click here</a>"
        )

    def test_image_node_with_none_url(self):
        node_image = TextNode("Image", "image", None)
        self.assertEqual(
            node_image.to_html(), "<img alt='Image' />"
        )

    def test_empty_text(self):
        node_text = TextNode("", "text")
        self.assertEqual(node_text.to_html(), "")


if __name__ == "__main__":
    unittest.main()
