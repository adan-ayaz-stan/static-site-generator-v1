class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        tmp_str = ""

        if self.props is None:
            return ""

        for key, value in self.props.items():
            tmp_str += f" {key}='{value}'"
        
        return tmp_str
    
    def __repr__(self) -> str:
        return f"Node({self.tag}, {self.value}, {self.children}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, children, tag, value=None, props=None) -> None:
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        tmp_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            tmp_str += child.to_html()
        tmp_str += f"</{self.tag}>"
        return tmp_str

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, children=None, props=None) -> None:
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"