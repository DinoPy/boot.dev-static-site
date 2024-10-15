import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_no_(self):
        with self.assertRaises(ValueError) as context:
            node = HTMLNode()

        self.assertEqual(str(context.exception),
                         "value or children must be provided")

    def test_print(self):
        node = HTMLNode("h1", "Title", None, {"title": "Cool title"})
        self.assertEqual(
            node.__repr__(), "HTMLNode(h1, Title, [], {'title': 'Cool title'})")

    def test_props_to_html(self):
        node = HTMLNode("p", "Contents", None, {"style": "font-size: 0.8em"})
        self.assertEqual(
            node.props_to_html(), '{"style": "font-size: 0.8em"}')

    def test_only_tag_passed(self):
        node = HTMLNode(value="thing")
        self.assertEqual(
            node.__repr__(), "HTMLNode(None, thing, [], None)")
