import tempfile
from unittest import TestCase

from vatu.config import Config
from vatu.hardware.power import set_power_limit, get_power_limit
from vatu.hardware.tests import get_filepath


class TestPower(TestCase):

    def test_get_power_limit(self):
        Config.update({'files': {'power': get_filepath('power1_cap')}})
        self.assertEqual(get_power_limit(), 123)

    def test_set_power_limit(self):
        with tempfile.NamedTemporaryFile('w') as f:
            Config.update({'files': {'power': f.name}})
            Config.update({'readonly': False})

            set_power_limit(100)
            self.assertEqual(get_power_limit(), 100)

            # make sure we honor read-only mode
            Config.update({'readonly': True})
            set_power_limit(99)
            self.assertEqual(get_power_limit(), 100)

            # make sure we honor the power limit
            Config.update({'readonly': False})
            Config.update({'card': {'power': {'limit': 150}}})
            with self.assertRaises(ValueError):
                set_power_limit(200)
            self.assertEqual(get_power_limit(), 100)
