# -*- coding: utf-8 -*-
import datetime
import tempfile
import unittest

from vatu.model.db import DB


class TmpDatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        DB.PATH = cls.tmpdir.name

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()


class TestRun(TmpDatabaseTestCase):
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

        # DB.delete(me)

    def test_traversal(self):
        """ Very basic check for uuid sanitization
        """
        path = DB._path_for_uuid('/etc/../test')
        self.assertNotIn('..', path)
        self.assertNotIn('/etc', path)
