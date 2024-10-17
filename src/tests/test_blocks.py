from unittest import TestCase
from src.blocks import MarkdownTypes,  markdown_to_blocks, block_to_block_type, markdown_to_html_node

final_content = """
# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```
"""


class TestBlocks(TestCase):
    def test_markdown_to_blocks(self):
        result = markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item""")

        self.assertListEqual(result,
                             ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

    def test_block_to_block_type(self):
        self.assertEqual(MarkdownTypes.PARAGRAPH, block_to_block_type(
            " This is a paragraph of text. It has some **bold** and *italic* words inside of it."))
        self.assertEqual(MarkdownTypes.HEADING,
                         block_to_block_type("# This is a heading"))
        self.assertEqual(MarkdownTypes.CODE, block_to_block_type(
            "```This is a heading```"))
        self.assertEqual(MarkdownTypes.UNORDERED_LIST,
                         block_to_block_type("- This is a heading"))
        self.assertEqual(MarkdownTypes.ORDERED_LIST,
                         block_to_block_type("1. This is a heading"))
        self.assertEqual(MarkdownTypes.QUOTE,
                         block_to_block_type("> This is a heading"))

    def test_markdown_to_html_node(self):
        result = markdown_to_html_node(final_content)
        print(result)
