import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_print(self):
        node = TextNode(None, TextType.TEXT)
        self.assertEqual(node.__repr__(), "TextNode(None, text, None)")

    def test_no_text(self):
        with self.assertRaises(TypeError) as context:
            node = TextNode("Title")
        self.assertEqual(str(context.exception),
                         "TextNode.__init__() missing 1 required positional argument: 'text_type'")

    def test_wrong_type(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("Title", "type")
        self.assertEqual(
            str(context.exception), "type must be an instance of TextType")

    def test_text_node_to_html_node(self):
        node1 = TextNode("this should be a bold element", TextType.BOLD)
        self.assertEqual(
            str(text_node_to_html_node(node1)),
            'LeafNode(b, this should be a bold element, None)')

        node2 = TextNode("this should be a raw element", TextType.TEXT)
        self.assertEqual(
            str(text_node_to_html_node(node2)),
            'LeafNode(None, this should be a raw element, None)')

        node3 = TextNode("this should be a italic element", TextType.ITALIC)
        self.assertEqual(
            str(text_node_to_html_node(node3)),
            'LeafNode(i, this should be a italic element, None)')

        node4 = TextNode("this should be a code element", TextType.CODE)
        self.assertEqual(
            str(text_node_to_html_node(node4)),
            'LeafNode(code, this should be a code element, None)')

        node5 = TextNode("this should be a link element",
                         TextType.LINK, "https://google.com")
        self.assertEqual(
            str(text_node_to_html_node(node5)),
            "LeafNode(a, this should be a link element, {'href': 'https://google.com'})")

        node6 = TextNode("this should be an image element",
                         TextType.IMAGE, "https://google.com")
        self.assertEqual(
            str(text_node_to_html_node(node6)),
            "LeafNode(img, this should be an image element, "
            "{'src': 'https://google.com', "
            "'alt': 'this should be an image element'})")


if __name__ == "__main__":
    unittest.main()
