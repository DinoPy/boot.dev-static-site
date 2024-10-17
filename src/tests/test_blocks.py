from unittest import TestCase
from src.blocks import markdown_to_blocks


class TestBlocks(TestCase):
    def test_markdown_to_blocks(self):
        markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item""")

