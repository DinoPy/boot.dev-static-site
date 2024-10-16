from src.htmlnode import LeafNode
import unittest


class TestLeafNode(unittest.TestCase):
    def test_no_value_init(self):
        with self.assertRaises(ValueError) as context:
            leaf_node = LeafNode(tag="h1")
        self.assertEqual(
            str(context.exception), "Value is mandatory")

    def test_to_html(self):
        node1 = LeafNode(value="value")
        self.assertEqual(node1.to_html(), "value")
        node2 = LeafNode("h1", "value",)
        self.assertEqual(node2.to_html(), "<h1>value</h1>")
        node3 = LeafNode("h1", "value", {"style": "font-size:0.8em"})
        self.assertEqual(
            node3.to_html(), "<h1 style=\"font-size:0.8em\">value</h1>")
