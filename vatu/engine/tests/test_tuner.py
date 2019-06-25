from unittest import TestCase
from unittest.mock import patch

from vatu.engine.tests.test_state import mock_state
from vatu.engine.tuner import SpeedyTuner


class TestSpeedyTuner(TestCase):

    @patch('vatu.engine.tuner.State')
    def test_speedy_tuner(self, mock_states):
        """ Basic scenario: get the p-level stable, but too low, raise power limit then raise clock
        """
        states = []

        state = mock_state()
        states.append(state)

        state = mock_state()
        states.append(state)

        state = mock_state()
        states.append(state)

        state = mock_state()
        state.core_plevel = 5
        states.append(state)

        state = mock_state()
        state.core_plevel = 5
        states.append(state)

        state = mock_state()
        state.core_plevel = 5
        states.append(state)

        mock_states.side_effect = states

        tuner = SpeedyTuner()

        try:
            while True:
                tuner.tick()
        except StopIteration:
            actions = tuner.actions
            self.assertEqual('Noop(unstable p-level)', str(actions[0]))
            self.assertEqual('Noop(unstable p-level)', str(actions[1]))
            self.assertEqual('SetCoreClock(1580)', str(actions[2]))
            self.assertEqual('SetPowerLimit(220)', str(actions[3]))
            self.assertEqual('Noop(unstable p-level)', str(actions[4]))
            self.assertEqual('Noop(unstable p-level)', str(actions[5]))
            self.assertEqual('SetCoreClock(1610)', str(actions[6]))
