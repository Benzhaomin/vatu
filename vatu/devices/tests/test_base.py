# -*- coding: utf-8 -*-
import unittest

from vatu.devices.base import DummyDevice


class TestDevice(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.device = DummyDevice()

    def test_read_sensor(self):
        self.assertEqual(self.device.read_sensor('sensor-1'), 0.0)
        self.assertEqual(self.device.read_sensor('sensor-2'), 0.0)
        with self.assertRaises(NotImplementedError):
            self.device.read_sensor('sensor-3')

    def test_read_sensors(self):
        self.assertEqual(self.device.read_sensors(), {
            'sensor-1': 0.0,
            'sensor-2': 0.0,
        })

    def test_read_setting(self):
        self.assertEqual(self.device.read_setting('setting-1'), 0.0)
        self.assertEqual(self.device.read_setting('setting-2'), 0.0)
        with self.assertRaises(NotImplementedError):
            self.device.read_sensor('setting-3')

    def test_read_settings(self):
        self.assertEqual(self.device.read_settings(), {
            'setting-1': 0.0,
            'setting-2': 0.0,
        })


