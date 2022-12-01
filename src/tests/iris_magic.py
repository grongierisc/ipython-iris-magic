# test module for iris_magic.py

import unittest

from iris_magic import IrisMagic


class TestIrisMagic(unittest.TestCase):

    def test_iris_magic(self):
        magic = IrisMagic()
        self.assertTrue(magic)
