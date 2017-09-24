# -*- coding: utf-8 -*-
import argparse

import sys


def cli(args):
    print("welcome")


def parse_args(args):
    parser = argparse.ArgumentParser()

    return parser.parse_args(args)


def main():
    cli(parse_args(sys.argv[1:]))


if __name__ == "__main__":
    main()
