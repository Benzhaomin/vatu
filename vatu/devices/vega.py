# -*- coding: utf-8 -*-
from vatu.devices.base import Device


class Vega(Device):
    name = 'Vega'
    sensors = [
        'core-voltage',  # mV
        'core-clock',  # MHz
        'core-power',  # W
        'card-power',  # W
    ]
    settings = [
        'core-voltage',  # mV
        'core-clock',  # MHz
        'memory-clock',  # MHz
        'power-limit',  # %
    ]

    def read_sensor(self, name):
        # TODO: use a lib to get actual values
        if name == 'core-voltage':
            return 1.0
        elif name == 'core-clock':
            return 1550.0
        elif name == 'core-power':
            return 140.0
        elif name == 'card-power':
            return 198.2
        return super().read_sensor(name)

    def read_setting(self, name):
        # TODO: use a lib to get actual values
        if name == 'core-voltage':
            return 1.04
        elif name == 'core-clock':
            return 1632.0
        elif name == 'memory-clock':
            return 1100.0
        elif name == 'power-limit':
            return 0.5
        return super().read_sensor(name)
