import unittest

from harlequin.hello import greet


class TestHello(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World!")
