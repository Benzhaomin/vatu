# -*- coding: utf-8 -*-
import unittest
import datetime

from vatu.db import DB


class TestRun(unittest.TestCase):
    def test_db(self):
        """ Simple save/load/delete test
        """
        me = {
            'uuid': 'db-test-run',
            'str': 'abc',
            'int': 123,
            'float': 123.25,
            'date': datetime.datetime.now(),
            'list': [
                'test'
            ],
            'dict': {
                'this': 'that',
            },
        }

        DB.save(me)

        loaded = DB.load('db-test-run')
        self.assertEqual(loaded, me)

        DB.delete(me)

    def test_traversal(self):
        """ Very basic check for uuid sanitization
        """
        path = DB._path_for_uuid('/etc/../test')
        self.assertNotIn('..', path)
        self.assertNotIn('/etc', path)
