# -*- coding: utf-8 -*-
import datetime
import time
import logging

from vatu.db import DB
from vatu.run import Run

logger = logging.getLogger('vatu.runner')


class Runner:
    @staticmethod
    def record(device, duration=60, interval=5):
        """ Record sensors values from *device* every *interval* seconds during *duration* seconds
        """
        run = Run()
        run['start'] = datetime.datetime.now()
        run['duration'] = duration
        run['settings'] = device.read_settings()
        run['datapoints'] = []
        DB.save(run)
        logger.info('Started a %s seconds Run', duration)

        while not Runner._finished(run):
            loop_start = datetime.datetime.now()

            # add current sensors values to datapoints
            datapoint = {'date': loop_start}
            datapoint.update(device.read_sensors())
            run['datapoints'].append(datapoint)
            DB.save(run)

            # sleep unless we're done recording
            if not Runner._finished(run):
                loop_has_taken = datetime.datetime.now() - loop_start
                time.sleep(interval - loop_has_taken.total_seconds())

        run['end'] = datetime.datetime.now()
        DB.save(run)

        return run

    @staticmethod
    def _finished(run):
        return datetime.datetime.now() - run['start'] >= datetime.timedelta(seconds=run['duration'])
