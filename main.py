#!/usr/bin/env python
from dotgen import config

import argparse


def run(args):
    pass


def list_configs(args):
    pass


def list_templates(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_run = subparsers.add_parser("run", help="generate dotfiles")
    parser_configs = subparsers.add_parser(
        "configs", help="list configurations")
    parser_templates = subparsers.add_parser(
        "templates", help="list templates")

    parser_run.set_defaults(func=run)
    parser_configs.set_defaults(func=list_configs)
    parser_templates.set_defaults(func=list_templates)

    args = parser.parse_args()
    args.func()
