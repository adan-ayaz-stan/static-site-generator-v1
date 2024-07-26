from src.htmlnode import HTMLNode, LeafNode, ParentNode


# Create a class for text nodes
class TextNode:
    def __init__(self, text, text_type, url=None):
        allowed_types = ["text", "bold", "italic", "code", "link", "image"]

        if text_type not in allowed_types:
            raise Exception(f"Unsupported text type: {text_type}")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(textnode_1, textnode_2):
        # return true if all props of the two text nodes are equal
        return (
            textnode_1.text == textnode_2.text
            and textnode_1.text_type == textnode_2.text_type
            and textnode_1.url == textnode_2.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html(self):
        # We're raising exception by not allowing construction of a TextNode with an unsupported text type

        if self.text_type == "text":
            return LeafNode(self.text)

        if self.text_type == "bold":
            return LeafNode(self.text, "b")

        if self.text_type == "italic":
            return LeafNode(self.text, "i")

        if self.text_type == "code":
            return LeafNode(self.text, "code")

        if self.text_type == "link":
            if self.url is None:
                return LeafNode(self.text, "a", None, {"href": "#"})

            return LeafNode(self.text, "a", None, {"href": self.url})

        if self.text_type == "image":
            if self.url is None:
                return LeafNode(None, "img", None, {"alt": self.text})
            return LeafNode(None, "img", None, {"src": self.url, "alt": self.text})
