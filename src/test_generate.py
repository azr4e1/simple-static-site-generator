import generate
import unittest


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.extract_title_ok = [
            (
                "\n\n# ciao",
                "ciao"
            ),
            (
                "# ciao\n\ncome va",
                "ciao"
            ),
            (
                "## ciao\n\ncome va\n\n# tutto bene",
                "tutto bene"
            ),
            (
                "## ciao\n\ncome va\n\n#tutto\n\n# bene",
                "bene"
            ),
        ]
        self.extract_title_error = [
            "## ciao",
            "#ciao\n\ncome va",
            "ciao"
            "",
            "tutto\n# bene"
            "ciao# ciao\n\ncome va\n\n#tutto\n\n#bene",
        ]

    def test_extract_title_ok(self):
        for test, case in self.extract_title_ok:
            result = generate.extract_title(test)
            self.assertEqual(result, case)

    def test_extract_title_error(self):
        for test in self.extract_title_error:
            self.assertRaises(Exception, generate.extract_title, test)


if __name__ == "__main__":
    unittest.main()
