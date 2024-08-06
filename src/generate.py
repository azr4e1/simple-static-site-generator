from pathlib import Path
import os
from shutil import rmtree, copy
from converter import markdown_to_html_node


_TITLE_PATTERN = "{{ Title }}"
_CONTENT_PATTERN = "{{ Content }}"
_MARKDOWN_SUFFIX = '.md'
_HTML_SUFFIX = '.html'


def recursive_copy(dst: str | Path, src: str | Path) -> None:
    src_path = Path(src)
    if not src_path.exists():
        raise Exception(f"source path '{src_path}' does not exist")
    dst_path = Path(dst)
    if dst_path.exists():
        rmtree(dst_path)

    dst_path.mkdir()
    content = os.listdir(src)
    for el in content:
        full_el_src_path = src_path / Path(el)
        full_el_dst_path = dst_path / Path(el)
        if full_el_src_path.is_dir():
            recursive_copy(full_el_dst_path, full_el_src_path)
        else:
            print(f" * {full_el_src_path} -> {full_el_dst_path}")
            copy(full_el_src_path, full_el_dst_path)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n\n")
    prefix = '# '
    for line in lines:
        clean_line = line.strip()
        if clean_line.startswith(prefix):
            return clean_line.removeprefix(prefix)

    raise Exception("markdown contains no title")


def generate_page(from_path: str | Path,
                  template_path: str | Path,
                  dest_path: str | Path) -> None:
    print("Generating page from "
          f"{from_path} to {dest_path} using {template_path}")
    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)
    if not from_path.exists() or not from_path.is_file():
        raise Exception("source file does not exist")
    if not template_path.exists() or not template_path.is_file():
        raise Exception("template file does not exist")

    content = from_path.read_text()
    template = template_path.read_text()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace(_TITLE_PATTERN, title)
    template = template.replace(_CONTENT_PATTERN, html_content)
    os.makedirs(dest_path.parent, exist_ok=True)
    dest_path.write_text(template)


def generate_pages_recursive(dir_path_content: str | Path,
                             template_path: str | Path,
                             dest_dir_path: str | Path) -> None:
    dir_path_content = Path(dir_path_content)
    template_path = Path(template_path)
    dest_dir_path = Path(dest_dir_path)
    if not dir_path_content.exists() or not dir_path_content.is_dir():
        raise Exception(f"{dir_path_content} is not a directory")

    files = os.listdir(dir_path_content)
    for el in files:
        full_el_path = dir_path_content / Path(el)
        full_dest_path = dest_dir_path / Path(el)
        if full_el_path.is_dir():
            generate_pages_recursive(full_el_path,
                                     template_path,
                                     full_dest_path)
        else:
            if full_el_path.suffix == _MARKDOWN_SUFFIX:
                generate_page(full_el_path,
                              template_path,
                              full_dest_path.with_suffix(_HTML_SUFFIX))
