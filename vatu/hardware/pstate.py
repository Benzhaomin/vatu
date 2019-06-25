from typing import Tuple, List

from vatu.config import Config

# (level, clock, active)
from vatu.sudo import sudo_cat

PState = Tuple[int, int, bool]


def parse_pstate(line: str) -> PState:
    """ Returns a pstate line as a 3-tuple of level, clock, active
    """
    parts = line.split()
    level = int(parts[0][0])
    clock = int(parts[1].replace('Mhz', ''))
    active = len(parts) > 2
    return level, clock, active


def read_pstates(filepath) -> List[PState]:
    """ Returns the power state table parsed
    """
    raw = sudo_cat(filepath)
    return list(map(parse_pstate, raw))


def get_active_pstate(filepath) -> PState:
    """ Returns the current power state (level, clock)
    """
    pstates = read_pstates(filepath)
    for p in pstates:
        if p[2]:
            return p[0:2]


def get_core_plevel() -> int:
    """ Returns the current core PowerPlay level
    """
    pstate_filepath = Config.get('files.core')
    return get_active_pstate(pstate_filepath)[0]


def get_memory_plevel() -> int:
    """ Returns the current memory PowerPlay level
    """
    pstate_filepath = Config.get('files.memory')
    return get_active_pstate(pstate_filepath)[0]
