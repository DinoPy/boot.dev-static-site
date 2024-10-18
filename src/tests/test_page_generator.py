import os
from unittest import TestCase
from src.page_generator import extract_title, generate_page

final_markdown = """# Tolkien Fan Club

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
```"""


class TestPageGenerator(TestCase):
    def test_extract_title(self):
        print(extract_title(final_markdown))
        self.assertEqual(extract_title(final_markdown), "Tolkien Fan Club")
        self.assertEqual(extract_title("# H1 title"), "H1 title")
        with self.assertRaises(Exception) as context:
            extract_title(" bla bla")
        self.assertEqual(str(context.exception), "The document has no title")
        with self.assertRaises(Exception) as context:
            extract_title("")
        self.assertEqual(str(context.exception), "invalid markdown")

    def test_generate_page(self):
        cwd = os.getcwd()
        generate_page(os.path.join(cwd, "content", "index.md"),
                      os.path.join(cwd, "template.html"),
                      os.path.join(cwd, "public", "index.html"))
