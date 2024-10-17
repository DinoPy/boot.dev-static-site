import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_no_(self):
        node = HTMLNode()
        self.assertEqual(str(node),
                         "HTMLNode(None, None, None, None)")

    def test_print(self):
        node = HTMLNode("h1", "Title", None, {"title": "Cool title"})
        self.assertEqual(
            node.__repr__(), "HTMLNode(h1, Title, None, {'title': 'Cool title'})")

    def test_props_to_html(self):
        node = HTMLNode("p", "Contents", None, {"style": "font-size: 0.8em"})
        self.assertEqual(
            node.props_to_html(), ' style="font-size: 0.8em"')

    def test_only_tag_passed(self):
        node = HTMLNode(value="thing")
        self.assertEqual(
            node.__repr__(), "HTMLNode(None, thing, None, None)")


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(
        ), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_init_without_tag(self):
        with self.assertRaises(TypeError) as context:
            node = ParentNode(children=[LeafNode("b", "Bold text")])
        self.assertEqual(
            str(context.exception), "ParentNode.__init__() missing 1 required positional argument: 'tag'")

    def test_init_without_children(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("h1", [])
            node.to_html()
        self.assertEqual(str(context.exception),
                         "a parent element can't be parent without children elements")

    def test_parent_within_parent(self):
        node = ParentNode("div", [LeafNode("h1", "Title")])
        node2 = ParentNode("div", [LeafNode("h1", "Title"), node])
        self.assertEqual(
            str(node2), "HTMLNode(div, None, [LeafNode(h1, Title, None), HTMLNode(div, None, [LeafNode(h1, Title, None)], None)], None)")

    def test_parent_within_parent_to_html(self):
        node = ParentNode("div", [LeafNode("h1", "Title")])
        node2 = ParentNode("div", [LeafNode("p", "paragraph"), node])

        self.assertEqual(
            node2.to_html(), "<div><p>paragraph</p><div><h1>Title</h1></div></div>")
