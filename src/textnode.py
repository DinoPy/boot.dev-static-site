from enum import Enum
from re import findall
from src.htmlnode import LeafNode
# TextType = Enum("types", ["Normal", "Bold",
# "Italic", "Code", "Links", "Images"])


class TextType(Enum):
    TEXT = "text"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
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


def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("Text type must be of TextType_Enum type")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.BOLD:
            return LeafNode("b",  text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_list = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            final_list.append(node)
            continue

        splits = node.text.split(delimiter)
        splits = list(filter(lambda x: len(x) > 0, splits))
        if len(splits) == 2:
            raise Exception("closing delimiter not found")
        if len(splits) == 1:
            final_list.append(TextNode(splits[0], TextType.TEXT))
            continue

        final_list.append(TextNode(splits[0], TextType.TEXT))
        final_list.append(TextNode(splits[1], text_type))
        final_list.append(TextNode(splits[2], TextType.TEXT))
    return final_list


def extract_markdown_images(text):
    # returns (alt, url)
    url_matches = findall(r"(?<=\().+?(?=\))", text)
    alt_matches = findall(r"(?<=\[).+?(?=\])", text)
    if len(url_matches) != len(alt_matches):
        raise Exception("The given markdown doesn't have matching alt & url")
    final_list = []
    for i in range(len(url_matches)):
        final_list.append((alt_matches[i], url_matches[i]))
    return final_list


def split_nodes_link_helper(text):
    if "(" in text:
        match = extract_markdown_images(text)
        return TextNode(match[0][0], TextType.LINK, match[0][1])
    else:
        return TextNode(text, TextType.TEXT)


def split_nodes_link(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue
        handle_text = node.text
        in_link = False
        while True:
            if in_link:
                i = handle_text.find(")")
                if i == -1:
                    break
                final_list.append(split_nodes_link_helper(handle_text[:i+1]))
                in_link = False
                handle_text = handle_text[i+1:]
            else:
                i = handle_text.find("[")
                if i == -1:
                    break
                final_list.append(split_nodes_link_helper(handle_text[:i]))
                in_link = True
                handle_text = handle_text[i:]
        if len(handle_text) > 1:
            final_list.append(split_nodes_link_helper(handle_text))

    return final_list


def split_nodes_image(old_nodes):
    for node in old_nodes:
        split_text = []
        handle_text = node.text
        in_link = False
        while True:
            if in_link:
                i = handle_text.find(")")
                if i == -1:
                    break
                split_text.append(handle_text[:i+1])
                in_link = False
                handle_text = handle_text[i+1:]
            else:
                i = handle_text.find("![")
                if i == -1:
                    break
                split_text.append(handle_text[:i])
                in_link = True
                handle_text = handle_text[i:]
        if len(handle_text) > 1:
            split_text.append(handle_text)

    final_list = []
    for text in split_text:
        if "![" in text:
            match = extract_markdown_images(text)
            final_list.append(
                TextNode(match[0][0], TextType.IMAGE, match[0][1]))
        else:
            final_list.append(TextNode(text, TextType.TEXT))
    return final_list


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    image_split = split_nodes_image([node])
    link_split = split_nodes_link(image_split)
    after_delimiter = split_nodes_delimiter(link_split, "`", TextType.CODE)
    after_delimiter2 = split_nodes_delimiter(
        after_delimiter, "**", TextType.BOLD)
    after_delimiter3 = split_nodes_delimiter(
        after_delimiter2, "*", TextType.ITALIC)
    return after_delimiter3
