# -*- coding: utf-8 -*-
from unittest.mock import patch

from vatu.device import DummyDevice
from vatu.runner import Runner
from vatu.tests.test_db import TmpDatabaseTestCase


class TestRunner(TmpDatabaseTestCase):
    @patch('time.sleep')
    def test_record(self, sleep):
        device = DummyDevice()
        run = Runner.record(device, 0.01, 0.001)

        self.assertIsNotNone(run['start'])
        self.assertIsNotNone(run['end'])
        self.assertIsNotNone(run['settings'])
        self.assertGreater(len(run['datapoints']), 0)
        self.assertGreater(sleep.call_count, 0)
