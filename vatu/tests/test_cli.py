# -*- coding: utf-8 -*-
import unittest

from vatu.cli import cli, parse_args


class TestCLI(unittest.TestCase):
    def test_parse_args(self):
        """ check args parsing
        """
        args = parse_args([])
        self.assertIsNotNone(args)

    def test_cli(self):
        """ check CLI invocation
        """
        cli([])
