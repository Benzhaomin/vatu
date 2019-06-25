from unittest import TestCase

from vatu.config import Config
from vatu.hardware.gpuinfo import get_gpu_power_usage, get_gpu_temperature, get_core_voltage, get_core_clock, \
    get_memory_clock
from vatu.hardware.tests import get_filepath


class TestGPUInfo(TestCase):
    @classmethod
    def setUpClass(cls):
        Config.update({'files': {'gpuinfo': get_filepath('amdgpu_pm_info')}})

    def test_read_power_usage(self):
        self.assertEqual(get_gpu_power_usage(), 4)

    def test_read_gpu_temperature(self):
        self.assertEqual(get_gpu_temperature(), 26)

    def test_read_gpu_load(self):
        self.assertEqual(get_gpu_temperature(), 26)

    def test_read_core_voltage(self):
        self.assertEqual(get_core_voltage(), 975)

    def test_read_core_clock(self):
        self.assertEqual(get_core_clock(), 27)

    def test_read_memory_clock(self):
        self.assertEqual(get_memory_clock(), 945)
