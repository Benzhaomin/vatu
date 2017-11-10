# -*- coding: utf-8 -*-
import datetime
import logging
import time

from vatu.model.db import DB
from vatu.model.run import Run

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
        logger.info('Started a %s seconds run', duration)

        while not Runner._finished(run):
            loop_start = datetime.datetime.now()

            # add current sensors values to datapoints
            datapoint = {'date': loop_start}
            datapoint.update(device.read_sensors())
            run['datapoints'].append(datapoint)
            DB.save(run)
            logger.debug('Datapoint recorded')

            # sleep unless we're done recording
            if not Runner._finished(run):
                sleep_duration = interval - (datetime.datetime.now() - loop_start).total_seconds()
                logger.debug('Sleeping for %s seconds', sleep_duration)
                time.sleep(sleep_duration)

        run['end'] = datetime.datetime.now()
        DB.save(run)
        logger.info('Run finished')

        return run

    @staticmethod
    def _finished(run):
        return datetime.datetime.now() - run['start'] >= datetime.timedelta(seconds=run['duration'])
