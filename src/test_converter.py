import unittest
from converter import markdown_to_html_node
from pathlib import Path
from htmlnode import ParentNode, LeafNode


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter_test = [
            (
                """# Hello

this is

- a markdown
- file

1. **come va**
2. tutto *bene*

![ciao](bello) this is a [link](google.com)

```
this is a block
node
```

> and
> this
> is a *quote*
                """,
                ParentNode('div', [
                    ParentNode('h1', [LeafNode('Hello')]),
                    ParentNode('p', [LeafNode('this is')]),
                    ParentNode('ul', [ParentNode('li', [LeafNode('a markdown')]),
                                      ParentNode('li', [LeafNode('file')]),
                                      ]),
                    ParentNode('ol', [
                        ParentNode('li', [LeafNode('come va', 'b')]),
                        ParentNode('li', [LeafNode('tutto '),
                                          LeafNode('bene', 'i')]),
                    ]),
                    ParentNode('p', [LeafNode('', 'img', props={'alt': 'ciao', 'src': 'bello'}),
                                     LeafNode(' this is a '),
                                     LeafNode('link', 'a', props={
                                              'href': 'google.com'})
                                     ]),
                    ParentNode(
                        'pre', [ParentNode('code', [LeafNode('\nthis is a block\nnode\n')])]),
                    ParentNode('blockquote', [LeafNode('and\nthis\nis a '),
                                              LeafNode('quote', 'i')])
                ])
            ),
            (
                """# Hello

this is

- a markdown
- file

1. `come va`
2. tutto *bene*

![ciao](bello) this is a [link](google.com)

```
this is a block
node
```

> and
> this
> is a *quote*
                """,
                ParentNode('div', [
                    ParentNode('h1', [LeafNode('Hello')]),
                    ParentNode('p', [LeafNode('this is')]),
                    ParentNode('ul', [ParentNode('li', [LeafNode('a markdown')]),
                                      ParentNode('li', [LeafNode('file')]),
                                      ]),
                    ParentNode('ol', [
                        ParentNode('li', [LeafNode('come va', 'code')]),
                        ParentNode('li', [LeafNode('tutto '),
                                          LeafNode('bene', 'i')]),
                    ]),
                    ParentNode('p', [LeafNode('', 'img', props={'alt': 'ciao', 'src': 'bello'}),
                                     LeafNode(' this is a '),
                                     LeafNode('link', 'a', props={
                                              'href': 'google.com'})
                                     ]),
                    ParentNode(
                        'pre', [ParentNode('code', [LeafNode('\nthis is a block\nnode\n')])]),
                    ParentNode('blockquote', [LeafNode('and\nthis\nis a '),
                                              LeafNode('quote', 'i')])
                ])
            ),
            (
                """# Hello

this is

- a markdown
- file

1. `come va`
2. tutto *bene*

![ciao](bello) this is a [link](google.com)

```
this is a block
node
```

> and
>this
> is a *quote*
                """,
                ParentNode('div', [
                    ParentNode('h1', [LeafNode('Hello')]),
                    ParentNode('p', [LeafNode('this is')]),
                    ParentNode('ul', [ParentNode('li', [LeafNode('a markdown')]),
                                      ParentNode('li', [LeafNode('file')]),
                                      ]),
                    ParentNode('ol', [
                        ParentNode('li', [LeafNode('come va', 'code')]),
                        ParentNode('li', [LeafNode('tutto '),
                                          LeafNode('bene', 'i')]),
                    ]),
                    ParentNode('p', [LeafNode('', 'img', props={'alt': 'ciao', 'src': 'bello'}),
                                     LeafNode(' this is a '),
                                     LeafNode('link', 'a', props={
                                              'href': 'google.com'})
                                     ]),
                    ParentNode(
                        'pre', [ParentNode('code', [LeafNode('\nthis is a block\nnode\n')])]),
                    ParentNode('p', [LeafNode('> and'), LeafNode(
                        '>this'), LeafNode('> is a '), LeafNode('quote', 'i')])
                ])
            ),
            (
                """# Hello

this is

- a markdown

2. tutto *bene*

![ciao](bello) this is a [link](google.com)

`ok`
this is a block
node
``#

> and
> this
> is a *quote*
                """,
                ParentNode('div', [
                    ParentNode('h1', [LeafNode('Hello')]),
                    ParentNode('p', [LeafNode('this is')]),
                    ParentNode('ul', [ParentNode('li', [LeafNode('a markdown')]),
                                      ]),
                    ParentNode('p', [LeafNode('2. tutto '),
                                     LeafNode('bene', 'i')]),
                    ParentNode('p', [LeafNode('', 'img', props={'alt': 'ciao', 'src': 'bello'}),
                                     LeafNode(' this is a '),
                                     LeafNode('link', 'a', props={
                                              'href': 'google.com'})
                                     ]),
                    ParentNode(
                        'p', [LeafNode('ok', 'code'),
                              LeafNode('this is a block'),
                              LeafNode('node'),
                              LeafNode('#')]),
                    ParentNode('blockquote', [LeafNode('and\nthis\nis a '),
                                              LeafNode('quote', 'i')])
                ])
            ),
        ]
        self.converter_test_error = [
            (
                """# Hello

this is

- a markdown
- file

1. *come va**
2. tutto *bene*

![ciao](bello) this is a [link](google.com)

```
this is a block
node
```

> and
> this
> is a *quote*
                """,
                ValueError, "invalid markdown syntax ('**' not closed)"
            ),
            (
                """# Hello

this is

- a markdown
- file

1. `come va`
2. tutto *bene*

![ciao](bello) this is a [link](google.com)

`
this is a block
node
```

> and
> this
> is a *quote*
                """,
                ValueError, "invalid markdown syntax ('`' not closed)"
            ),
            (
                """# Hello

this is

- a markdown

2. tutto *bene*

![ciao](bello) this is a [link](google.com)

`ok`
this is a block
node
``#

> and
> this
> is a *quote
                """, ValueError, "invalid markdown syntax ('*' not closed)"

            ),
        ]

    def test_converter(self):
        for test, case in self.converter_test:
            result = markdown_to_html_node(test)
            self.assertEqual(result, case)

    def test_converter_error(self):
        for test, exception, msg in self.converter_test_error:
            with self.assertRaises(exception) as m:
                markdown_to_html_node(test)
            self.assertEqual(msg, m.exception.args[0])
