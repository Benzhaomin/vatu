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
