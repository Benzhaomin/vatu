import unittest

from vatu.devices.vega import Vega


class TestVega(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.device = Vega()

    def test_read_sensors(self):
        # TODO: mock the sensors lib
        self.assertIsNotNone(self.device.read_sensors())

    def test_read_settings(self):
        # TODO: mock the sensors lib
        self.assertIsNotNone(self.device.read_settings())