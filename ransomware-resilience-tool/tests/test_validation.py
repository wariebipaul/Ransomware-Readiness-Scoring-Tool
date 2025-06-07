import unittest
from src.utils.validation import validate_input

class TestValidation(unittest.TestCase):

    def test_validate_input_valid(self):
        self.assertTrue(validate_input("valid input"))

    def test_validate_input_invalid(self):
        self.assertFalse(validate_input(""))

    def test_validate_input_numeric(self):
        self.assertTrue(validate_input("12345"))

    def test_validate_input_special_characters(self):
        self.assertFalse(validate_input("!@#$%"))

if __name__ == '__main__':
    unittest.main()