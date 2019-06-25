""" Provides a uniform interface to hardware settings like voltage and clocks
"""

from typing import Any

from vatu.hardware import power, powerplay


class Setting:
    @staticmethod
    def get() -> Any:
        return

    @staticmethod
    def set(value: Any):
        pass


class PowerLimit(Setting):
    @staticmethod
    def get():
        return power.get_power_limit()

    @staticmethod
    def set(value):
        power.set_power_limit(value)


class CorePPTable(Setting):
    @staticmethod
    def get():
        return powerplay.get_powerplay_table('core')

    @staticmethod
    def set(value):
        powerplay.set_powerplay_table('core', value)


class MemoryPPTable(Setting):
    @staticmethod
    def get():
        return powerplay.get_powerplay_table('memory')

    @staticmethod
    def set(value):
        powerplay.set_powerplay_table('memory', value)
