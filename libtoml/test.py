import unittest

from libtoml import parse


class ParseTest(unittest.TestCase):

    def test_empty(self):
        data = parse("")
        self.assertEqual(data, {})

    def test_comment(self):
        data = parse("# This is a comment")
        self.assertEqual(data, {})

    def test_comment_inline(self):
        contents = """
        key = "Title" # this is a comment
        """
        data = parse(contents)
        self.assertEqual(data["key"], "Title")

    def test_string(self):
        contents = """
        key = "Title"
        """
        data = parse(contents)
        self.assertEqual(data["key"], "Title")

    def test_string_hash(self):
        contents = """
        channel = "#python"
        """
        data = parse(contents)
        self.assertEqual(data["channel"], "#python")

    def test_integer(self):
        contents = """
        key = 42
        """
        data = parse(contents)
        self.assertEqual(data["key"], 42)

    def test_integer_negative(self):
        contents = """
        key = -42
        """
        data = parse(contents)
        self.assertEqual(data["key"], -42)

    def test_float(self):
        contents = """
        key = -42.0
        """
        data = parse(contents)
        self.assertEqual(data["key"], -42.0)

    def test_boolean_false(self):
        contents = """
        key = false
        """
        data = parse(contents)
        self.assertEqual(data["key"], False)

    def test_boolean_true(self):
        contents = """
        key = true
        """
        data = parse(contents)
        self.assertEqual(data["key"], True)

    def test_list(self):
        contents = """
        key = [ 8001, 8001, 8002 ]
        """
        data = parse(contents)
        self.assertEqual(data["key"], [8001, 8001, 8002])

    def test_list_trailing_comma(self):
        contents = """
        key = [ 8001, 8001, 8002, ]
        """
        data = parse(contents)
        self.assertEqual(data["key"], [8001, 8001, 8002])

    def test_array(self):
        contents = """
        [database]
        server = "192.168.1.1"
        ports = [ 8001, 8001, 8002 ]
        connection_max = 5000
        enabled = true
        default = -42
        """
        data = parse(contents)
        self.assertEqual(data["database"]["server"], "192.168.1.1")
        self.assertEqual(data["database"]["connection_max"], 5000)

    def test_array_nested(self):
        contents = """
        [x.y.z]
        """
        data = parse(contents)
        self.assertEqual(data["x"]["y"]["z"], {})

    def test_array_nested_values(self):
        contents = """
        [x.y.z]
        start = "now"
        """
        data = parse(contents)
        self.assertEqual(data["x"]["y"]["z"]["start"], "now")

    def test_array_nested_defined(self):
        contents = """
        [servers]

          # You can indent as you please. Tabs or spaces. TOML don't care.
          [servers.alpha]
          ip = "10.0.0.1"
          dc = "eqdc10"

          [servers.beta]
          ip = "10.0.0.2"
          dc = "eqdc10"
        """

        data = parse(contents)
        self.assertEqual(data["servers"]["alpha"]["ip"], "10.0.0.1")

    def test_list_inline(self):
        contents = """
        [clients]
        data = [ ["gamma", "delta"], [1, 2] ]
        """
        data = parse(contents)
        self.assertEqual(data["clients"]["data"][0][0], "gamma")
        self.assertEqual(data["clients"]["data"][1][0], 1)

    def test_list_linebreaks(self):
        contents = """
        #  Line breaks are OK when inside arrays
        hosts = [
          "alpha",
          "omega",
        ]
        """
        data = parse(contents)
        self.assertEqual(data["hosts"][0], "alpha")
        self.assertEqual(data["hosts"][1], "omega")

    def test_dict_literal(self):
        contents = """
        book = {"name": "Book", "price": "6.50"}
        """
        data = parse(contents)
        self.assertEqual(data["book"]["name"], "Book")

    def test_dict_literal_lines(self):
        contents = """
        book = {
            "name": "Book",
            "price": "6.50",
        }
        """
        data = parse(contents)
        self.assertEqual(data["book"]["name"], "Book")

    def test_dict_trailing_comma(self):
        contents = """
        book = {"name": "Book", "price": "6.50", }
        """
        data = parse(contents)
        self.assertEqual(data["book"]["name"], "Book")

    def test_array_dict(self):
        contents = """
        products = [
            {"name": "Book", "price": "6.50", },
            {"name": "Bell", "price": "0.50"},
            {1: 2, 3.0: "0.50"}, # trailing comma, no problem
        ]
        """
        data = parse(contents)
        self.assertEqual(data["products"][0]["name"], "Book")

    def test_key_format(self):
        contents = """
        channel#hello? = "#python"
        """
        data = parse(contents)
        self.assertEqual(data["channel#hello?"], "#python")


if __name__ == "__main__":
    unittest.main()
