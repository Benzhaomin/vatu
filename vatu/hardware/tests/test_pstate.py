from unittest import TestCase

from vatu.config import Config
from vatu.hardware.pstate import get_core_plevel, get_memory_plevel
from vatu.hardware.tests import get_filepath


class TestPState(TestCase):

    def test_get_core_plevel(self):
        Config.update({'files': {'core': get_filepath('pp_dpm_sclk')}})
        level = get_core_plevel()
        self.assertEqual(level, 0)

    def test_get_memory_plevel(self):
        Config.update({'files': {'memory': get_filepath('pp_dpm_mclk')}})
        level = get_memory_plevel()
        self.assertEqual(level, 3)
