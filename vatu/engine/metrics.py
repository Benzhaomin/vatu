import json
import logging
import os
import time
from typing import List

from vatu.config import Config

# timestamp, name, value
Metric = dict


def get_metric(name, value, timestamp=None) -> Metric:
    """ Returns a new metric dict
    """
    if not timestamp:
        timestamp = time.time()
    timestamp = int(round(timestamp * 1000000))

    return {
        'name': name,
        'value': value,
        'timestamp': timestamp,
    }


def persist(metrics: List[Metric]) -> str:
    """ Write metrics as Sensision metrics to disk, can be consumed by Beamium
    """
    outputdir = Config.get('metrics.outputdir')
    os.makedirs(outputdir, exist_ok=True)
    filename = 'vatu-{}.metrics'.format(int(round(time.time() * 1000000)))

    with open(os.path.join(outputdir, filename), 'w') as f:
        for metric in metrics:
            logging.debug(json.dumps(metric))
            datapoint = '{timestamp}// {name}{{}} {value}'.format(**metric)
            print(datapoint, file=f)

    return filename
