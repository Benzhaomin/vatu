from vatu.config import Config
from vatu.sudo import sudo_tee, sudo_cat


def get_power_limit() -> int:
    """ Reads the card's power cap
    """
    powerfile = Config.get('files.power')
    lines = sudo_cat(powerfile)
    return int(int(lines[0]) / 10 ** 6)


def set_power_limit(limit: int):
    """ Set the card's power cap
    """
    power_limit = Config.get('card.power.limit')
    if int(limit) > power_limit:
        raise ValueError("requested power limit %s is higher than the config limit %s", limit, power_limit)

    power_filepath = Config.get('files.power')
    actual = limit * 10 ** 6
    sudo_tee(power_filepath, actual)
