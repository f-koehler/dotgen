#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs
import os
import subprocess
import sys

from dotgen import config
from dotgen import hashing
from dotgen import plugins


def diff(args):
    cfg, _ = config.read_config(
        os.path.join(args.config_dir, args.config + ".yml"))

    diffs = []

    dotfiles = config.render_dotfiles(args.template_dir, cfg)
    for dotfile_name in dotfiles:
        tmp_path = os.path.join("/tmp", "dotgen", dotfile_name)
        tmp_dir = os.path.dirname(tmp_path)
        output_path = os.path.join(args.output, dotfile_name)

        if not os.path.exists(output_path):
            continue

        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        with codecs.open(tmp_path, "w", "utf-8") as fhandle:
            fhandle.write(dotfiles[dotfile_name])

        cmd = [
            "git", "diff", "--color=always", "--no-index", "--", output_path,
            tmp_path
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, _ = process.communicate()

        out = out.decode()
        if out:
            diffs.append(out)

    if diffs:
        print("\n".join(diffs))


def generate(args):
    cfg, _ = config.read_config(
        os.path.join(args.config_dir, args.config + ".yml"))

    dotfiles = config.render_dotfiles(args.template_dir, cfg)

    dotfiles_old = {}
    for dotfile_name in dotfiles:
        output_path = os.path.join(args.output, dotfile_name)

        if not os.path.exists(output_path):
            dotfiles_old[dotfile_name] = dotfiles[dotfile_name]
            continue

        hash_new = hashing.hash_string(dotfiles[dotfile_name])
        hash_old = hashing.hash_file(output_path)

        if hash_new != hash_old:
            dotfiles_old[dotfile_name] = dotfiles[dotfile_name]

    if not dotfiles_old:
        return

    if not args.force:
        print("Files that will be (over)written:")
        for dotfile_name in dotfiles_old:
            print("\t" + os.path.join(args.output, dotfile_name))

        if sys.version_info < (3, 0):
            confirmation = raw_input(
                "Is this what you want? (y/n) ").strip().lower()
        else:
            confirmation = input(
                "Is this what you want? (y/n) ").strip().lower()
        if confirmation.lower() != "y":
            return

    for dotfile_name in dotfiles_old:
        template_file_path = os.path.join(args.template_dir, dotfile_name)
        output_path = os.path.join(args.output, dotfile_name)
        dir_name = os.path.dirname(output_path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with codecs.open(output_path, "w", "utf-8") as fhandle:
            fhandle.write(dotfiles_old[dotfile_name])

        permissions = os.stat(template_file_path)
        os.chmod(output_path, permissions[0])


def list_configs(args):
    configs = config.list_configs(args.config_dir)
    for cfg in configs:
        print(cfg)


def list_templates(args):
    templates = config.list_templates(args.template_dir)
    for template in templates:
        print(template)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument(
        "--config-dir", default=config.get_default_config_dir())
    parser.add_argument(
        "--template-dir", default=config.get_default_template_dir())

    parser_configs = subparsers.add_parser(
        "configs", help="list configurations")
    parser_configs.set_defaults(func=list_configs)

    parser_diff = subparsers.add_parser(
        "diff", help="show diff between generated and existent files")
    parser_diff.set_defaults(func=diff)
    parser_diff.add_argument("-o", "--output", default=config.get_home_dir())
    parser_diff.add_argument("config")

    parser_generate = subparsers.add_parser(
        "generate", help="generate dotfiles")
    parser_generate.set_defaults(func=generate)
    parser_generate.add_argument("-f", "--force", action="store_true")
    parser_generate.add_argument(
        "-o", "--output", default=config.get_home_dir())
    parser_generate.add_argument("config")

    parser_plugins = subparsers.add_parser("plugins", help="execute plugins")
    parser_plugins.set_defaults(func=execute_plugins)
    parser_plugins.add_argument(
        "-o", "--output", default=config.get_home_dir())
    parser_plugins.add_argument("config")

    parser_templates = subparsers.add_parser(
        "templates", help="list templates")
    parser_templates.set_defaults(func=list_templates)

    args = parser.parse_args()
    args.func(args)


def execute_plugins(args):
    _, plugin_cfg = config.read_config(
        os.path.join(args.config_dir, args.config + ".yml"))
    plugins.handle_plugins(args.output, plugin_cfg)


if __name__ == "__main__":
    main()
