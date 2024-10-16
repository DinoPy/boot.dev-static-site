from enum import Enum
# TextType = Enum("types", ["Normal", "Bold",
# "Italic", "Code", "Links", "Images"])


class TextType(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINKS = "links"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        if not isinstance(text_type, TextType):
            raise ValueError("type must be an instance of TextType")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self, text_node):
        pass

