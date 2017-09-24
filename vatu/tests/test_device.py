# -*- coding: utf-8 -*-
import unittest

from vatu.device import Device, Vega


class DeviceZero(Device):
    name = 'Device Zero'
    sensors = ['sensor-1', 'sensor-2']
    settings = ['setting-1', 'setting-2']

    def read_sensor(self, name):
        if name in self.sensors:
            return 0.0
        return super().read_sensor(name)

    def read_setting(self, name):
        if name in self.settings:
            return 0.0
        return super().read_setting(name)


class TestDevice(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.device = DeviceZero()

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
