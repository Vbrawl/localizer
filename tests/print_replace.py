from typing import IO
import unittest
from localizer.print_replace import print as _print


class fake_file(IO):
    def __init__(self, max_buffer = -1):
        self.writes = []
        self.max_buffer = max_buffer

    def write(self, val):
        if self.max_buffer != -1 and self.max_buffer < len(val):
            val = val[:self.max_buffer]
        self.writes.append(val)
        return len(val)
    
    def read(self):
        return self.writes


class TestPrintFunctionArguments(unittest.TestCase):
    def test_sep(self):
        with self.assertRaises(TypeError):
            _print("Hello", file=fake_file(), sep=1) # type: ignore
    
    def test_end(self):
        with self.assertRaises(TypeError):
            _print("Hello", file=fake_file(), end=1) # type: ignore

    def test_file(self):
        with self.assertRaises(AttributeError):
            _print("Hello", file=2) # type: ignore


class TestPrintFunctionEmulation(unittest.TestCase):
    def test_print_simple(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", file=f1)
        print("Hello", file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_print_multiple_values(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", "World", file=f1)
        print("Hello", "World", file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_print_multiple_different_typed_values(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", 2, [1, 2, 3], file=f1)
        print("Hello", 2, [1, 2, 3], file=f2)
        self.assertEqual(f1.read(), f2.read())
    

    def test_print_simple_buffered(self):
        f1 = fake_file(2)
        f2 = fake_file(2)
        _print("Hello", file=f1)
        print("Hello", file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_print_multiple_values_buffered(self):
        f1 = fake_file(2)
        f2 = fake_file(2)
        _print("Hello", "World", file=f1)
        print("Hello", "World", file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_print_multiple_different_typed_values_buffered(self):
        f1 = fake_file(2)
        f2 = fake_file(2)
        _print("Hello", 2, [1, 2, 3], file=f1)
        print("Hello", 2, [1, 2, 3], file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_None_end(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", end=None, file=f1)
        print("Hello", end=None, file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_null_end(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", end='', file=f1)
        print("Hello", end='', file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_None_sep(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", sep=None, file=f1)
        print("Hello", sep=None, file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_null_sep(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", sep='', file=f1)
        print("Hello", sep='', file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_None_end_multiple_values(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", "World", "Hiii", end=None, file=f1)
        print("Hello", "World", "Hiii", end=None, file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_null_end_multiple_values(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", "World", "Hiii", end='', file=f1)
        print("Hello", "World", "Hiii", end='', file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_None_sep_multiple_values(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", "World", "Hiii", sep=None, file=f1)
        print("Hello", "World", "Hiii", sep=None, file=f2)
        self.assertEqual(f1.read(), f2.read())
    
    def test_null_sep_multiple_values(self):
        f1 = fake_file()
        f2 = fake_file()
        _print("Hello", "World", "Hiii", sep='', file=f1)
        print("Hello", "World", "Hiii", sep='', file=f2)
        self.assertEqual(f1.read(), f2.read())


if __name__ == "__main__":
    unittest.main()