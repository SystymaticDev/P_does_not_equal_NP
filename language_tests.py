# language_tests.py
import unittest
from core_language import LanguageInterpreter

class TestLanguageInterpreter(unittest.TestCase):
    def test_print_command(self):
        interp = LanguageInterpreter()
        parsed = interp.parse("PRINT Hello World")
        self.assertEqual(parsed, [("PRINT", ["Hello", "World"])])
        # We might also test execute() here if we redirect stdout
