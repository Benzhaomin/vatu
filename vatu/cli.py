# -*- coding: utf-8 -*-
import argparse
import sys
import time
import logging

from vatu.runner import Runner


def record(args):
    if args.get('delay'):
        logging.info('Delaying start for %s seconds', args.get('delay'))
        time.sleep(args.get('delay'))

    # TODO: support other devices
    from vatu.devices.vega import Vega
    device = Vega()
    Runner.record(device)


COMMANDS = {
    'record': record,
}


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)

    subparsers = parser.add_subparsers(help="command")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--delay", type=int, help="start recording after delay seconds")

    return vars(parser.parse_args(argv))


def setup_logging(verbosity):
    if verbosity >= 2:
        loglevel = logging.DEBUG
    elif verbosity == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    logging.basicConfig(level=loglevel, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def main():
    args = parse_args(sys.argv[1:])
    setup_logging(args.get('verbose'))

    try:
        COMMANDS.get('record')(args)
    except IndexError:
        print("Please provide a command name")


if __name__ == "__main__":
    main()
