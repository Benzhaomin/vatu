import time
from unittest import TestCase
from unittest.mock import MagicMock, patch

from vatu.engine.state import State


def mock_state():
    state = MagicMock(spec=State)
    state.timestamp = time.time()

    # GPU sensors and settings
    state.gpu_temperature = 30
    state.gpu_load = 99
    state.gpu_power_usage = 200
    state.gpu_power_limit = 210

    # Core sensors and settings
    state.core_clock = 1600
    state.core_voltage = 1150
    state.core_plevel = 4
    state.core_pptable = [(900, 900), (950, 930), (1000, 950), (1200, 1000), (1500, 1100), (1600, 1200)]
    state.core_pstate = (1650, 1200)
    state.core_ppclock = 1650
    state.core_ppvoltage = 1200

    # Memory sensors
    state.memory_clock = 945
    state.memory_plevel = 1
    state.memory_pptable = [(500, 800), (945, 1050)]
    state.memory_pstate = (945, 1050)
    state.memory_ppclock = 845
    state.memory_ppvoltage = 1050

    return state


class TestState(TestCase):

    @patch('vatu.engine.state.sensors')
    @patch('vatu.engine.state.settings')
    def test_init(self, settings, sensors):
        state = State()
        # just make sure we didn't try to actually read sensors and settings
        self.assertIsNotNone(state)

    def test_str(self):
        state = mock_state()
        state.__str__ = State.__str__
        self.assertIn('1600Mhz', str(state))
        self.assertIn('1650Mhz', str(state))
        self.assertIn('210W', str(state))
