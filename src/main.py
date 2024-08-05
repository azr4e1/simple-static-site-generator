import generate


def main():
    generate.recursive_copy('public', 'static')
    generate.generate_page(
        'content/index.md', 'template.html', 'public/index.html')


main()
