from pathlib import Path
import os
from shutil import rmtree, copy
# from converter import markdown_to_html_node


def recursive_copy(dst: str | Path, src: str | Path):
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
            copy(full_el_src_path, full_el_dst_path)


def main():
    recursive_copy('public', 'static')


main()
