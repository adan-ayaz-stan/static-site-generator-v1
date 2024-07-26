import unittest

from src.textnode import TextNode
from src.utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class UtilsTest(unittest.TestCase):

    # SPLIT NODES DELIMITER TESTS
    def test_split_nodes_delimiter_code_blocks(self):
        node_text = TextNode("This is text with a `code block` inbetween.", "text")
        self.assertEqual(
            split_nodes_delimiter([node_text], "`", "code"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" inbetween.", "text"),
            ],
        )

    def test_split_nodes_delimiter_multiple_nests(self):
        node_text = TextNode(
            "This is text with two `code block 1` and `code block 2` inbetween.", "text"
        )

        self.assertEqual(
            split_nodes_delimiter([node_text], "`", "code"),
            [
                TextNode("This is text with two ", "text"),
                TextNode("code block 1", "code"),
                TextNode(" and ", "text"),
                TextNode("code block 2", "code"),
                TextNode(" inbetween.", "text"),
            ],
        )

    # EXTRACT MARKDOWN IMAGES TESTS
    def test_extract_markdown_images_test_1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpg"),
            ],
        )

    def test_extract_markdown_images_basic(self):
        text = "This is an image ![alt text](http://example.com/image.jpg)"
        expected_output = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_extract_markdown_images_no_links(self):
        text = "This is a text without any image links."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_extract_markdown_images_multiple_links(self):
        text = "Here is one image ![alt1](http://example.com/image1.jpg) and here is another ![alt2](http://example.com/image2.jpg)"
        expected_output = [
            ("alt1", "http://example.com/image1.jpg"),
            ("alt2", "http://example.com/image2.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected_output)

    # EXTRACT MARKDOWN LINKS TESTS
    def test_extract_markdown_links_basic(self):
        text = "This is text with a [link](https://example.com) inbetween."
        expected_output = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_extract_markdown_links_no_links(self):
        text = "This is text without any links."
        expected_output = []
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_extract_markdown_links_multiple_links(self):
        text = "Here is one [link1](https://example.com) and here is another [link2](https://example.com)"
        expected_output = [
            ("link1", "https://example.com"),
            ("link2", "https://example.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_extract_markdown_links_multiple_nests(self):
        text = "This is text with two [link1](https://example.com) and [link2](https://example.com) inbetween."
        expected_output = [
            ("link1", "https://example.com"),
            ("link2", "https://example.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

    # SPLIT NODES IMAGE TESTS:
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )

        new_nodes = split_nodes_image([node])
        expected_output = [
            TextNode("This is text with an image ", "text"),
            TextNode("to boot dev", "image", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "image", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(new_nodes, expected_output)

    def test_no_images(self):
        # Test case where there are no images in the text
        old_nodes = [TextNode("Hello World", "text")]
        expected_output = old_nodes
        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_single_image(self):
        # Test case where there is a single image in the text
        old_nodes = [TextNode("Hello ![image](url) World", "text")]
        expected_output = [
            TextNode("Hello ", "text"),
            TextNode("image", "image", "url"),
            TextNode(" World", "text"),
        ]

        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_multiple_images(self):
        # Test case where there are multiple images in the text
        old_nodes = [TextNode("Hello ![image1](url1) World ![image2](url2)", "text")]
        expected_output = [
            TextNode("Hello ", "text"),
            TextNode("image1", "image", "url1"),
            TextNode(" World ", "text"),
            TextNode("image2", "image", "url2"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_consecutive_images(self):
        # Test case where there are consecutive images in the text
        old_nodes = [TextNode("Hello ![image1](url1) ![image2](url2) World", "text")]
        expected_output = [
            TextNode("Hello ", "text"),
            TextNode("image1", "image", "url1"),
            TextNode(" ", "text"),
            TextNode("image2", "image", "url2"),
            TextNode(" World", "text"),
        ]

        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    def test_empty_text(self):
        # Test case where the text is empty
        old_nodes = [TextNode("", "text")]
        expected_output = old_nodes
        self.assertEqual(split_nodes_image(old_nodes), expected_output)

    # SPLIT NODES LINK TESTS:

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )

        new_nodes = split_nodes_link([node])
        expected_output = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected_output)

    # MULTI INLINE TESTS:
    def test_multi_link_and_images(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) and a link [to boot dev](https://www.boot.dev)",
            "text",
        )

        expected_output = [
            TextNode("This is text with an image ", "text"),
            TextNode("to boot dev", "image", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "image", "https://www.youtube.com/@bootdotdev"),
            TextNode(" and a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
        ]

        self.assertEqual(split_nodes_link(split_nodes_image([node])), expected_output)
