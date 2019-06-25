import tempfile
from unittest import TestCase

from vatu.config import Config
from vatu.hardware.powerplay import get_powerplay_table, set_powerplay_table
from vatu.hardware.tests import get_filepath


class TestPowerPlayTable(TestCase):

    def test_get_powerplay_table(self):
        Config.update({'files': {'powerplay': get_filepath('pp_od_clk_voltage')}})
        table = get_powerplay_table('memory')
        self.assertEqual(table, [(167, 800), (500, 800), (800, 950), (1234, 1050)])

    def test_set_powerplay_table(self):
        with tempfile.NamedTemporaryFile('w+') as f:
            Config.update({'files': {'powerplay': f.name}})
            Config.update({'readonly': False})

            set_powerplay_table('core', [(1200, 800), (1400, 900)])
            self.assertEqual(f.readlines(), ['s 0 1200 800\n', 's 1 1400 900\n', 'c\n'])

        # make sure we honor the clock limit
        with tempfile.NamedTemporaryFile('w+') as f:
            Config.update({'files': {'powerplay': f.name}})
            Config.update({'core': {'clock': {'limit': 1650}}})
            Config.update({'core': {'voltage': {'limit': 1300}}})

            with self.assertRaises(ValueError):
                set_powerplay_table('core', [(1500, 1050), (1650, 1050), (1700, 1200)])
            self.assertEqual(f.readlines(), ['s 0 1500 1050\n', 's 1 1650 1050\n', 'r\n'])

        # make sure we honor the voltage limit
        with tempfile.NamedTemporaryFile('w+') as f:
            Config.update({'files': {'powerplay': f.name}})
            Config.update({'core': {'clock': {'limit': 1800}}})
            Config.update({'core': {'voltage': {'limit': 1100}}})

            with self.assertRaises(ValueError):
                set_powerplay_table('core', [(1600, 1050), (1650, 1100), (1700, 1200)])
            self.assertEqual(f.readlines(), ['s 0 1600 1050\n', 's 1 1650 1100\n', 'r\n'])

        # make sure we honor read-only mode
        with tempfile.NamedTemporaryFile('w+') as f:
            Config.update({'files': {'powerplay': f.name}})
            Config.update({'readonly': True})

            set_powerplay_table('core', [(1200, 800), (1400, 900)])
            self.assertEqual(f.readlines(), [])
