import unittest

class TestStringMethods(unittest.TestCase):

    def test_one_plus_one(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()