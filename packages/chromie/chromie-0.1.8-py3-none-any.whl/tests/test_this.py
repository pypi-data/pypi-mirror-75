import unittest
import sys
from unittest.mock import patch
import argparse

import chromie

import chromie.chromie

from chromie.chromie import parse_args

class TestArgumentParser(unittest.TestCase):

    def get_arguments(self, parser, test_args):
        with patch.object(sys, 'argv', test_args):
            args = parse_args(parser, sys.argv)
        return args

    def test_init_args(self):
        parser = argparse.ArgumentParser(prog='chromie_1')
        test_args = 'init . -n testy'.split()
        args = self.get_arguments(parser=parser, test_args=test_args)
        
        self.assertEqual(args.name, 'testy')
        self.assertEqual(args.command, 'init')
        self.assertEqual(args.filepath, '.')

    # def test_pack_args(self):
    #     parser = ArgumentParser(prog='chromie_2')
    #     test_args = 'pack ./testy'.split()
    #     with patch.object(sys, 'argv', test_args):
    #         args = chromie.parse_args(sys.argv)
    #         self.assertEqual(args.command, 'pack')
    #         self.assertEqual(args.filepath, './testy')
        

if __name__ == '__main__':
    unittest.main()