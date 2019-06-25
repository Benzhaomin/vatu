from vatu.engine import settings


class Action:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)

    def run(self):
        pass


class Noop(Action):
    pass


class SetPowerLimit(Action):
    def run(self):
        settings.PowerLimit.set(self.value)


class SetCoreClock(Action):
    def run(self):
        """ On Linux it seems we need to set P-State 5 to 7 or the card will just jump down a P-State
        """
        table = settings.CorePPTable.get()

        for i in [5, 6, 7]:
            table[i] = (self.value, table[i][1])

        settings.CorePPTable.set(table)


class SetCoreVoltage(Action):
    def run(self):
        """ On Linux it seems we need to set P-State 5 to 7 or the card will just jump down a P-State
        """
        table = settings.CorePPTable.get()

        for i in [5, 6, 7]:
            table[i] = (table[i][0], self.value)

            settings.CorePPTable.set(table)
