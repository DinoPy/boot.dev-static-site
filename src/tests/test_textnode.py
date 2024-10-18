import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes


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

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(new_nodes), "[TextNode(This is text with a , text, None), TextNode(code block, code, None), TextNode( word, text, None)]")

        node_italic = TextNode(
            "This is text with a **italic block** word", TextType.TEXT)
        new_nodes_italic = split_nodes_delimiter(
            [node_italic], "*", TextType.ITALIC)
        self.assertEqual(
            str(new_nodes_italic), "[TextNode(This is text with a , text, None), TextNode(italic block, italic, None), TextNode( word, text, None)]")

        node_bold = TextNode(
            "This is text with a **bold block** word", TextType.TEXT)
        new_nodes_bold = split_nodes_delimiter([node_bold], "*", TextType.BOLD)
        self.assertEqual(
            str(new_nodes_bold), "[TextNode(This is text with a , text, None), TextNode(bold block, bold, None), TextNode( word, text, None)]")

        # with self.assertRaises(Exception) as context:
        #     node_missing_delimiter = TextNode(
        #         "This is text with a **bold block word", TextType.TEXT)
        #     new_nodes_incomplete = split_nodes_delimiter(
        #         [node_missing_delimiter], "*", TextType.BOLD)
        # self.assertEqual(str(context.exception), "closing delimiter not found")

    def test_extract_markdown_images(self):
        result = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(str(result),
                         "[('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]")
        with self.assertRaises(Exception) as context:
            result1 = extract_markdown_images(
                "This is text with a link (https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(str(context.exception),
                         "The given markdown doesn't have matching alt & url")

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.TEXT, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])

        node2 = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes2 = split_nodes_image([node2])
        self.assertListEqual(new_nodes2, [
            TextNode("This is text with a link ", TextType.TEXT, None),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
