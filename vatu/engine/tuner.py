import logging
from typing import List, Optional

from vatu.config import Config
from vatu.engine import metrics
from vatu.engine.actions import Action, SetCoreClock, SetPowerLimit, Noop, SetCoreVoltage
from vatu.engine.state import State


class FeelTheVibeMixin:
    def core_plevel_recent_values(self, horizon=3) -> Optional[set]:
        if len(self.states) < horizon:
            return None
        return set([s.core_plevel for s in self.states[-horizon:]])

    def core_plevel_is_stable(self, horizon=3) -> Optional[bool]:
        plevels = self.core_plevel_recent_values(horizon)
        if not plevels:
            logging.debug('waiting to have more data point on core p-level stability')
            return None
        return len(plevels) == 1

    def gpu_load_too_low(self) -> bool:
        return self.current_state.gpu_load < Config.get('card.load.minimum')

    def gpu_temperature_is_too_high(self) -> bool:
        return self.current_state.gpu_temperature >= Config.get('card.temperature.limit')


class AbortTuningException(Exception):
    pass


class Tuner(FeelTheVibeMixin):
    def __init__(self):
        self.states: List[State] = []
        self.actions: List[Action] = []
        self.current_state: Optional[State] = None

    def tick(self):
        """ Do cool stuff, one tick at a time
        """
        self.sense()
        actions = self.think()
        if not actions:
            logging.warning("no action chosen after a lot of thinking, looks like a bug")
            return

        self.actions.extend(actions)
        for action in actions:
            self.act(action)

    def sense(self):
        """ Read sensors and current settings
        """
        self.current_state = State()
        logging.info(self.current_state)
        self.states.append(self.current_state)

        if Config.get('metrics.enabled'):
            metrics.persist(self.current_state.metrics())

    def think(self) -> List[Action]:
        """ Is this AI?
        """
        if self.gpu_temperature_is_too_high():
            logging.info("gpu temperature is too high")
            raise AbortTuningException('Aborting! GPU temperature too high')

        if self.gpu_load_too_low():
            logging.info("gpu load too low")
            raise AbortTuningException('Aborting! GPU load is too low')

        if not self.core_plevel_is_stable():
            logging.info("core p-level isn't stable, not doing anything this tick")
            return [Noop('unstable p-level')]

    def act(self, action: Action):
        """ Apply changes
        """
        try:
            action.run()
        except Exception:
            raise AbortTuningException('Aborting! Failed to run {}'.format(action))


class SpeedyTuner(Tuner):
    """ Raise core clock as high as possible

    - get the GPU in a stable state (stable p-level >= 5, lower core clock)
    - push core clock a little bit every tick
    - if we can't hold a p-level, push power limit or core voltage and lower core clock 2 steps
    - stop when we reach configuration limits (core clock, core voltage, power limit)
    """

    def think(self) -> List[Action]:
        actions = super().think()
        if actions:
            return actions

        # everything good, raise core clock
        if self.current_state.core_plevel >= 5:
            new_clock = self.current_state.core_pptable[-1][0] + Config.get('core.clock.step')
            logging.info("p-level stable and high enough, raising core clock to %sMHz", new_clock)
            return [SetCoreClock(new_clock)]
        # reaching power limit at a lower than p5/6/7 pstate, lower clock and raise power limit
        elif self.current_state.gpu_power_limit - self.current_state.gpu_power_usage < 20:
            new_clock = self.current_state.core_pptable[-1][0] - 2 * Config.get('core.clock.step')
            new_power = self.current_state.gpu_power_limit + int(Config.get('card.power.step'))
            logging.info("p-level stable but too low, close to power limit, raising power limit to %sW", new_power)
            return [
                SetCoreClock(new_clock),
                SetPowerLimit(new_power),
            ]
        # lack of core power, lower clock and raise core voltage
        else:
            new_clock = self.current_state.core_pptable[-1][0] - 2 * Config.get('core.clock.step')
            new_voltage = self.current_state.core_pptable[-1][1] + int(Config.get('core.voltage.step'))
            logging.info("p-level stable but too low, far from power limit, raising core voltage to %smV", new_voltage)
            return [
                SetCoreClock(new_clock),
                SetCoreVoltage(new_voltage),
            ]


class StarvingTuner(Tuner):
    """ With a fixed frequency (more or less 10%), we want to lower power usage

    - get the GPU in a stable state (stable p-level >= 5, raise power limit if necessary)
    - record Power usage / Core clock delta over time
    - lower the core voltage until we lose more mhz than watts
    """
    pass
