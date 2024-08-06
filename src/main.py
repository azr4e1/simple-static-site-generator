import generate


def main():
    generate.recursive_copy('public', 'static')
    generate.generate_pages_recursive('content', 'template.html', 'public')


main()
