from pathlib import Path
from converter import markdown_to_html_node


def main():
    data = Path("./testdata/test_converter/test1.md").read_text()
    node = markdown_to_html_node(data)
    print(node.to_html())


main()
