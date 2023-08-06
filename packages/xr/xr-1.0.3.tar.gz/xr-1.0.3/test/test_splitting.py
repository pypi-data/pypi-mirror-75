from unittest import TestCase

from xr import Text, WhiteSpace


class TestSplit(TestCase):
    def test_split(self):
        s = "duck duck goose more_ducks hyphenated-duck überduck"
        expected = s.split()
        self.assertEquals(WhiteSpace.split(s), expected)
        self.assertEquals(Text(" ").split(s), expected)
        
    
