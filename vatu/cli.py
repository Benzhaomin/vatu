# -*- coding: utf-8 -*-
import logging

import click

from vatu.config import Config
from vatu.engine.state import State
from vatu.engine.timer import timer
from vatu.engine.tuner import AbortTuningException, SpeedyTuner


def setup_logging(verbosity):
    if verbosity >= 2:
        loglevel = logging.DEBUG
    elif verbosity == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    logging.basicConfig(level=loglevel, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('-c', '--config', default=None, help="load configuration from this file")
def cli(verbose, config):
    """ Vega Auto Tuner
    """
    setup_logging(verbose)
    if config:
        Config.load(config)


@cli.command(short_help='try to reach a power, clock or temperature target')
@click.option('-d', '--duration', default=180)
@click.option('-i', '--interval', default=15)
def autotune(duration, interval):
    initial_state = State()
    logging.info('Initial state %s', initial_state)
    try:
        tuner = SpeedyTuner()
        timer(tuner.tick, duration, interval)
        final_state = State()
        logging.info('Reached final state %s', final_state)
    except AbortTuningException as exc:
        logging.error(str(exc))
    finally:
        logging.info('Restoring initial state %s', initial_state)
        initial_state.restore()


@cli.command(short_help="show the card's current state")
def show():
    state = State()
    print(state)


def main():
    cli()


if __name__ == "__main__":
    main()
