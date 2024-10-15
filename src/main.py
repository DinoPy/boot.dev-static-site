from textnode import TextType, TextNode


def main():
    node = TextNode("text", TextType.NORMAL, "url")
    print(node)


if __name__ == "__main__":
    main()
