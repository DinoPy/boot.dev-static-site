from enum import Enum
from re import match, sub
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import text_to_textnodes, text_node_to_html_node


class MarkdownTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    # takes raw markdown string and returns a list of block strings
    splits = markdown.split("\n\n")
    splits = list(map(lambda x: x.strip(), splits))
    return splits


def block_to_block_type(markdown_block):
    # returns block type
    if markdown_block.startswith("#"):
        return MarkdownTypes.HEADING
    if markdown_block.startswith("```"):
        return MarkdownTypes.CODE
    if markdown_block.startswith(">"):
        return MarkdownTypes.QUOTE
    if markdown_block.startswith("* ") or markdown_block.startswith("- "):
        return MarkdownTypes.UNORDERED_LIST
    if match(r"^\d.", markdown_block):
        return MarkdownTypes.ORDERED_LIST
    return MarkdownTypes.PARAGRAPH


def markdown_block_to_html(markdown_block):
    match block_to_block_type(markdown_block):
        case MarkdownTypes.PARAGRAPH:
            text_nodes = text_to_textnodes(markdown_block)
            children = []
            for n in text_nodes:
                children.append(text_node_to_html_node(n))
            return ParentNode("p", children)
        case MarkdownTypes.HEADING:
            heading_level = len(match(r"^#+", markdown_block).group(0))
            stripped_block = sub(r"^#+ ", "", markdown_block)
            stripped_inner_item = text_to_textnodes(stripped_block)
            children = []
            for n in stripped_inner_item:
                children.append(text_node_to_html_node(n))
            return ParentNode(f"h{heading_level}", children)
        case MarkdownTypes.CODE:
            stripped_block = markdown_block.replace("```", "")
            return ParentNode("div", [LeafNode("code", stripped_block)])
        case MarkdownTypes.QUOTE:
            stripped_block = markdown_block.replace(">", "")
            return ParentNode("div", [LeafNode("blockquote", stripped_block.strip())])
        case MarkdownTypes.ORDERED_LIST:
            list_items = markdown_block.split("\n")
            children_list = []
            for item in list_items:
                stripped_item = sub(r"^\d+.", "", item).strip()
                stripped_inner_item = text_to_textnodes(stripped_item)
                children = []
                for n in stripped_inner_item:
                    children.append(text_node_to_html_node(n))
                children_list.append(ParentNode("li", children))
            return ParentNode("ol", children=children_list)
        case MarkdownTypes.UNORDERED_LIST:
            list_items = markdown_block.split("\n")
            children_list = []
            for item in list_items:
                stripped_item = item.replace("* ", "").replace("- ", "")
                stripped_inner_item = text_to_textnodes(stripped_item)
                children = []
                for n in stripped_inner_item:
                    children.append(text_node_to_html_node(n))
                children_list.append(ParentNode("li", children))
            return ParentNode("ul", children=children_list)


def markdown_to_html_node(markdown):
    children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        children.append(markdown_block_to_html(block))
    return ParentNode("div", children=children)
