from typing import Optional, List

from vatu.config import Config
from vatu.sudo import sudo_cat


def get_raw_gpu_infos() -> List[str]:
    """ Returns the contents of amdgpu_pm_info
    """
    filepath = Config.get('files.gpuinfo')
    raw = sudo_cat(filepath)
    return list(map(str.strip, raw))


def get_gpu_info(needle: str) -> Optional[str]:
    """ Returns a single line of GPU Info if needle is found
    """
    for line in get_raw_gpu_infos():
        if needle in line:
            return line


def get_gpu_power_usage() -> float:
    """ Returns the current card power usage (W)
    """
    return float(get_gpu_info('average GPU').split()[0])


def get_gpu_temperature() -> int:
    """ Returns the current GPU Temperature (C)
    """
    return int(get_gpu_info('GPU Temperature').split()[-2])


def get_gpu_load() -> float:
    """ Returns the current GPU load (%)
    """
    return int(get_gpu_info('GPU Load').split()[-2])


def get_core_voltage() -> int:
    """ Returns the current core voltage (mV)
    """
    return int(get_gpu_info('VDDGFX').split()[0])


def get_core_clock() -> int:
    """ Returns the current core clock (MHz)
    """
    return int(get_gpu_info('SCLK').split()[0])


def get_memory_clock() -> int:
    """ Returns the current memory clock (MHz)
    """
    return int(get_gpu_info('MCLK').split()[0])
