import json


class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props=None):
        if not value and not children:
            raise ValueError("value or children must be provided")
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return json.dumps(self.props)
