import time
from typing import List

from vatu.engine import sensors, settings
from vatu.engine.metrics import get_metric, Metric


class State:
    def __init__(self):
        """ Build a new State based on current sensors and settings
        """
        self.timestamp = time.time()

        # GPU sensors and settings
        self.gpu_temperature = sensors.GpuTemperature.read()
        self.gpu_load = sensors.GpuLoad.read()
        self.gpu_power_usage = sensors.GpuPowerUsage.read()
        self.gpu_power_limit = settings.PowerLimit.get()

        # Core sensors and settings
        self.core_clock = sensors.CoreClock.read()
        self.core_voltage = sensors.CoreVoltage.read()
        self.core_plevel = sensors.CorePLevel.read()
        self.core_pptable = settings.CorePPTable.get()
        self.core_pstate = self.core_pptable[self.core_plevel]
        self.core_ppclock = self.core_pstate[0]
        self.core_ppvoltage = self.core_pstate[1]

        # Memory sensors
        self.memory_clock = sensors.MemoryClock.read()
        self.memory_plevel = sensors.MemoryPLevel.read()
        self.memory_pptable = settings.MemoryPPTable.get()
        self.memory_pstate = self.memory_pptable[self.memory_plevel]
        self.memory_ppclock = self.memory_pstate[0]
        self.memory_ppvoltage = self.memory_pstate[1]

    def __str__(self):
        gpu = '{:>3}% {:>2}C {:>5}W / {:>3}W'.format(self.gpu_load, self.gpu_temperature, self.gpu_power_usage,
                                                     self.gpu_power_limit)
        core = '{:>4}Mhz@{:>4}mV P{} {:>4}Mhz@{:>4}mV'.format(self.core_clock, self.core_voltage, self.core_plevel,
                                                              self.core_ppclock, self.core_ppvoltage)
        memory = '{:>4}Mhz P{} {:>4}Mhz@{:>4}mV'.format(self.memory_clock, self.memory_plevel, self.memory_ppclock,
                                                        self.memory_ppvoltage)

        return ' # '.join([gpu, core, memory])

    def restore(self):
        """ Restore the card back to this state's settings (power limit and Power Play tables)
        """
        settings.PowerLimit.set(self.gpu_power_limit)
        settings.CorePPTable.set(self.core_pptable)
        settings.MemoryPPTable.set(self.memory_pptable)

    def metrics(self) -> List[Metric]:
        return [
            get_metric('gpu.load', self.gpu_load),
            get_metric('gpu.temperature', self.gpu_temperature),
            get_metric('gpu.power_usage', self.gpu_power_usage),
            get_metric('core.clock', self.core_clock),
            get_metric('core.voltage', self.core_voltage),
            get_metric('core.plevel', self.core_plevel),
            get_metric('memory.clock', self.memory_clock),
            get_metric('memory.plevel', self.memory_plevel),
        ]
