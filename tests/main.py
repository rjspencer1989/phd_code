import unittest


class TestStringMethods(unittest.TestCase):
    
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('foo'.isupper())
        
if __name__ == '__main__':
    unittest.main()