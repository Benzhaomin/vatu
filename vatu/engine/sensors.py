""" Provides a uniform interface to a suite of hardware sensors
"""

from typing import Any

from vatu.hardware import gpuinfo, pstate


class Sensor:
    @staticmethod
    def read() -> Any:
        return


class GpuTemperature(Sensor):
    @staticmethod
    def read():
        return gpuinfo.get_gpu_temperature()


class GpuLoad(Sensor):
    @staticmethod
    def read():
        return gpuinfo.get_gpu_load()


class GpuPowerUsage(Sensor):
    @staticmethod
    def read():
        return gpuinfo.get_gpu_power_usage()


class CoreClock(Sensor):
    @staticmethod
    def read():
        return gpuinfo.get_core_clock()


class CoreVoltage(Sensor):
    @staticmethod
    def read():
        return gpuinfo.get_core_voltage()


class CorePLevel(Sensor):
    @staticmethod
    def read():
        return pstate.get_core_plevel()


class MemoryClock(Sensor):
    @staticmethod
    def read():
        return gpuinfo.get_memory_clock()


class MemoryPLevel(Sensor):
    @staticmethod
    def read():
        return pstate.get_memory_plevel()
