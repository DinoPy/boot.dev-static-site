import os
from src.blocks import markdown_to_html_node


def extract_title(markdown):
    if len(markdown) < 2:
        raise Exception("invalid markdown")
    split = markdown.split("\n\n")
    title = split[0]
    if not title.startswith("# "):
        raise Exception("The document has no title")
    return title[2:]


def generate_page(from_path, template_path, dest_path):
    print(f"GENERATING PAGE FROM: {from_path}\nUSING TEMPLATE: { template_path}\nTO DESTINATION: {dest_path}")
    with open(from_path) as file:
        contents = file.read()
    with open(template_path) as file:
        template = file.read()
    html_nodes = markdown_to_html_node(contents)
    html_string = html_nodes.to_html()
    title = extract_title(contents)
    final = template.replace("{{ Title }}", title)
    final = final.replace("{{ Content }}", html_string)
    with open(dest_path, "w") as f:
        f.write(final)


cwd = os.getcwd()
content_path = os.path.join(cwd, "content")
template_path = os.path.join(cwd, "template.html")
public_path = os.path.join(cwd, "public")


def generate_web(f=content_path, template=template_path, to=public_path):
    content_files = os.listdir(f)
    for item in content_files:
        if os.path.isfile(os.path.join(f, item)):
            if ".md" not in item:
                continue

            generate_page(os.path.join(f, item),
                          template,
                          os.path.join(to, "index.html"))
        if os.path.isdir(os.path.join(f, item)):
            os.mkdir(os.path.join(to, item))
            generate_web(os.path.join(f, item),
                         template,
                         os.path.join(to, item))
