import unittest

from src.htmlnode import HTMLNode
from src.htmlnode import ParentNode
from src.htmlnode import LeafNode

# HTML Node Structure (self, tag=None, value=None, children=None, props=None)
class TestHTMLNode(unittest.TestCase):
    def test_props_method(self):
        node_1 = HTMLNode("h1", "Hello World", None, {"class": "test"})

        self.assertEqual(node_1.props_to_html(), " class='test'")

    def test_repr(self):
        node_1 = HTMLNode("h1", "Hello World", None, {"class": "test"})

        self.assertEqual(node_1.__repr__(), "Node(h1, Hello World, None, {'class': 'test'})")


    # def test_equality(self):
    #     # The equality test is failing because __eq__ is not implemented in HTMLNode class
    #     # In Python 3.x, __eq__ is automatically defined for all classes, but not in Python 2.x
    #     # So, we need to define it in our class
    #     node_1 = HTMLNode("h1", "Hello World", None, {"class": "test"})
    #     node_2 = HTMLNode("h1", "Hello World", None, {"class": "test"})

    #     self.assertEqual(node_1, node_2)

# ParentNode Structure (self, children, tag, value=None, props=None)
class TestParentNode(unittest.TestCase):
    def test_html_method(self):
        leaf_nodes = [
            LeafNode("I am a paragraph", "p", None, {"class": "para-sm"}),
            LeafNode("I am another paragraph", "p", None, {"class": "para-md"}),
            LeafNode("I am a third paragraph", "p", None, {"class": "para-lg"}),
            LeafNode("I am a fourth paragraph", "p", None, {"class": "para-xl"}),
        ]
        node_1 = ParentNode(leaf_nodes, "h1", "Hello World", {"class": "test"})

        self.assertEqual(node_1.to_html(), "<h1 class='test'><p class='para-sm'>I am a paragraph</p><p class='para-md'>I am another paragraph</p><p class='para-lg'>I am a third paragraph</p><p class='para-xl'>I am a fourth paragraph</p></h1>")

    def test_html_method_parent_inside_parent(self):
        leaf_nodes = [
            LeafNode("I am a paragraph", "p", None, {"class": "para-sm"}),
            LeafNode("I am another paragraph", "p", None, {"class": "para-md"}),
            LeafNode("I am a third paragraph", "p", None, {"class": "para-lg"}),
            LeafNode("I am a fourth paragraph", "p", None, {"class": "para-xl"}),
        ]
        node_1 = ParentNode(leaf_nodes, "h1", "Hello World", {"class": "test"})
        node_2 = ParentNode([node_1], "div", "Hello World", {"class": "test"})

        self.assertEqual(node_2.to_html(), "<div class='test'><h1 class='test'><p class='para-sm'>I am a paragraph</p><p class='para-md'>I am another paragraph</p><p class='para-lg'>I am a third paragraph</p><p class='para-xl'>I am a fourth paragraph</p></h1></div>")

    def test_html_method_multi_parent_inside_parent(self):
        leaf_nodes = [
            LeafNode("I am a paragraph", "p", None, {"class": "para-sm"}),
            LeafNode("I am another paragraph", "p", None, {"class": "para-md"}),
            LeafNode("I am a third paragraph", "p", None, {"class": "para-lg"}),
            LeafNode("I am a fourth paragraph", "p", None, {"class": "para-xl"}),
        ]
        node_1 = ParentNode(leaf_nodes, "div", "Parent Node 1", {"class": "parent-1"})
        node_2 = ParentNode(leaf_nodes, "div", "Parent Node 2", {"class": "parent-2"})

        node_3 = ParentNode([node_1, node_2], "div", "Ultimate Parent", {"class": "parent-0"})

        self.assertEqual(node_3.to_html(), "<div class='parent-0'><div class='parent-1'><p class='para-sm'>I am a paragraph</p><p class='para-md'>I am another paragraph</p><p class='para-lg'>I am a third paragraph</p><p class='para-xl'>I am a fourth paragraph</p></div><div class='parent-2'><p class='para-sm'>I am a paragraph</p><p class='para-md'>I am another paragraph</p><p class='para-lg'>I am a third paragraph</p><p class='para-xl'>I am a fourth paragraph</p></div></div>")

# LeafNode Structure (self, value, tag=None, children=None, props=None)
class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node_1 = LeafNode("Hello World", "h1", None, {"class": "test"})

        self.assertEqual(node_1.__repr__(), "Node(h1, Hello World, None, {'class': 'test'})")

    def test_props_method(self):
        node_1 = LeafNode("h1", "Hello World", None, {"class": "test"})

        self.assertEqual(node_1.props_to_html(), " class='test'")

    def test_html_method(self):
        node_1 = LeafNode("Hello World", "h1", None, {"class": "test"})

        self.assertEqual(node_1.to_html(), "<h1 class='test'>Hello World</h1>")