# -*- coding: utf-8 -*-
import unittest

from vatu.run import Run


class TestRun(unittest.TestCase):
    def test_init(self):
        # new Run
        run = Run()
        self.assertIsNotNone(run['uuid'])

        # loading an existing Run
        run = Run({'uuid': '1234'})
        self.assertEqual(run['uuid'], '1234')
