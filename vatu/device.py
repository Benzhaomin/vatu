# -*- coding: utf-8 -*-


class Device:
    name = 'Dummy'
    sensors = []
    settings = []

    def read_sensor(self, name):
        """ Returns the current value of a sensor

        :returns float
        """
        raise NotImplementedError("No such sensor %s".format(name))

    def read_sensors(self):
        return {
            name: self.read_sensor(name) for name in self.sensors
        }

    def read_setting(self, name):
        """ Returns the current value of a setting

        :returns float
        """
        raise NotImplementedError("No such setting %s".format(name))

    def read_settings(self):
        return {
            name: self.read_setting(name) for name in self.settings
        }


class DummyDevice(Device):
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
