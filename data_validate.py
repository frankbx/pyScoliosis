# -*- coding: utf-8 -*-
# !/bin/env python
import unittest


class TestDataValidator(unittest.TestCase):
    def testValidateInteger(self):
        v = StringDataValidator("123")
        self.assertTrue(v.validate_integer())
        v = StringDataValidator("12.3")
        self.assertFalse(v.validate_integer())
        v = StringDataValidator("12o")
        self.assertFalse(v.validate_integer())

    def testValidateFloat(self):
        v = StringDataValidator("12.3")
        self.assertTrue(v.validate_float())
        v = StringDataValidator("12。3")
        self.assertFalse(v.validate_float())


class StringDataValidator:
    def __init__(self, data):
        self.data = data

    def validate_integer(self):
        try:
            x = int(self.data)
            return True
        except ValueError:
            return False

    def validate_float(self):
        try:
            x = float(self.data)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    unittest.main()
