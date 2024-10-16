import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_print(self):
        node = TextNode(None, TextType.NORMAL)
        self.assertEqual(node.__repr__(), "TextNode(None, normal, None)")

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


if __name__ == "__main__":
    unittest.main()
