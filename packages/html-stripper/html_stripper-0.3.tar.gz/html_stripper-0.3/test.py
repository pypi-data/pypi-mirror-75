import unittest
from html_stripper import strip_tags


class TestStripper(unittest.TestCase):
    def test_title(self):
        """
        <title> is skipped
        """
        data = "<html><head><title>a</title></head><body>b</body></html>"
        expected = "b"
        result = strip_tags(data)
        self.assertEqual(result, expected)

    def test_comment(self):
        """
        comments are skipped
        """
        data = "<html><head><title>…</title><!-- a --></head><!-- c --><body>b<!-- d --></body></html>"
        expected = "b"
        result = strip_tags(data)
        self.assertEqual(result, expected)

    def test_style(self):
        """
        styles are skipped
        """
        data = """<html><head><title>a</title><style>body {color: hoptink;}</style>
                  </head><body>b<style>body {background: white;}</style></body></html>"""
        expected = "b"
        result = strip_tags(data)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
