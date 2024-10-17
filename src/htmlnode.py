import json


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError(
            "to_html method will be implemented in children classes")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_string = ""
        for prop in self.props:
            props_string += f' {prop}="{self.props[prop]}"'
        return props_string


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value="", props=None):
        if not value:
            raise ValueError("Value is mandatory")
        super().__init__(tag=tag, value=value, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.tag is None:
            return self.value
        prop_string = ""
        if self.props:
            for p in self.props:
                prop_string += f" {p}=\"{self.props[p]}\""

        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent element must have a tag")
        if len(self.children) < 1:
            raise ValueError(
                "a parent element can't be parent without children elements")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()

        prop_string = ""
        if self.props:
            for p in self.props:
                prop_string += f" {p}=\"{self.props[p]}\""

        return f'<{self.tag}{prop_string}>{children_string}</{self.tag}>'
