from typing import Tuple, List

from vatu.config import Config
from vatu.sudo import sudo_tee_a, sudo_cat

TABLES = {
    # friendly name: (name when reading, prefix when setting a p-state)
    'core': ('OD_SCLK', 's'),
    'memory': ('OD_MCLK', 'm'),
}

PowerState = Tuple[int, int]  # clock Mhz, voltage mV
PowerPlayTable = List[PowerState]


def read_raw_powerplay_tables() -> List[str]:
    """ Reads the PowerPlay clock/voltage file *pp_od_clk_voltage*
    """
    powerplay_filepath = Config.get('files.powerplay')
    raw = sudo_cat(powerplay_filepath)
    return list(map(str.strip, raw))


def get_powerplay_table(name: str) -> PowerPlayTable:
    """ Returns a PowerPlay table as a list of clock/voltage tuples
    """
    raw_name = TABLES[name][0]
    raw_tables = read_raw_powerplay_tables()
    table = []
    consuming = False

    for line in raw_tables:
        if line.startswith(raw_name):
            consuming = True
            continue
        if consuming:
            try:
                int(line[0])
            except ValueError:
                # found something other than a number, we read the whole table, exit
                break
            raw = line.split()
            table.append((int(raw[1].replace('Mhz', '')), int(raw[2].replace('mV', ''))))

    return table


def set_powerplay_table(name: str, table: PowerPlayTable):
    """ Updates and commits a PowerPlay table from list of clock/voltage tuples

    Global config limits are respected / out of limits p-states are ignored
    """
    powerplay_filepath = Config.get('files.powerplay')
    prefix = TABLES[name][1]
    clock_limit = Config.get('{}.clock.limit'.format(name))
    voltage_limit = Config.get('{}.voltage.limit'.format(name))

    for level, (clock, voltage) in enumerate(table):
        # apply limits
        if clock > clock_limit:
            sudo_tee_a(powerplay_filepath, 'r')
            raise ValueError('ignored p-state over the %s clock limit %s MHz > %s MHz', name, clock, clock_limit)

        if voltage > voltage_limit:
            sudo_tee_a(powerplay_filepath, 'r')
            raise ValueError('ignored p-state over the %s voltage limit %s mV > %s mV', name, voltage, voltage_limit)

        # update the p-state
        raw_pstate = '{prefix} {level:d} {clock:d} {voltage:d}'.format(prefix=prefix, level=level, clock=clock,
                                                                       voltage=voltage)
        sudo_tee_a(powerplay_filepath, raw_pstate)

    # commit (really apply changes to the card)
    sudo_tee_a(powerplay_filepath, 'c')
