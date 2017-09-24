# -*- coding: utf-8 -*-
import argparse

import sys

from vatu.run import Run
from vatu.runner import Runner


def cli(args):
    if args.command == 'run':
        run = Run()
        Runner.run(run)


def parse_args(args):
    parser = argparse.ArgumentParser()

    return parser.parse_args(args)


def main():
    cli(parse_args(sys.argv[1:]))


if __name__ == "__main__":
    main()
