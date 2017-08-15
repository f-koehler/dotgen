#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import jinja2
import yaml

import argparse
import codecs
import logging
import os
import shutil
import subprocess
import sys

dotfiles_dir = os.path.join(os.path.expanduser("~"), ".dotfiles")
template_dir = os.path.join(dotfiles_dir, "templates")
config_dir = os.path.join(dotfiles_dir, "configs")
loader = jinja2.FileSystemLoader(template_dir)
templates = loader.list_templates()
environment = jinja2.Environment(loader=loader)


def get_template_list():
    templates = []
    for root, _, files in os.walk(template_dir):
        for file in files:
            templates.append(
                os.path.relpath(os.path.join(root, file), template_dir))
    return templates


def get_gitmodule_list(config):
    if "gitmodules" not in config:
        return []

    return [gitmodule for gitmodule in config["gitmodules"]]


def get_symlink_list(config):
    if "symlinks" not in config:
        return []

    return [symlink for symlink in config["symlink"]]


def get_number_of_tasks(config):
    return len(get_template_list()) + len(get_gitmodule_list(config)) + len(
        get_symlink_list(config))


def render_dotfiles(render_dir, config):
    config_path = os.path.join(dotfiles_dir, "configs", config + ".yml")
    with codecs.open(config_path, "r", "utf-8") as fh:
        config = yaml.load(fh)

    for template_name in templates:
        template_path = os.path.join(template_dir, template_name)
        template = environment.get_template(template_name)
        logging.info("render \"%s\"", template_name)
        rendered = template.render(config=config)
        if rendered.splitlines():
            output_path = os.path.join(render_dir, template_name)
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                logging.info("create directory \"%s\"", output_dir)
                os.makedirs(output_dir)
            with codecs.open(output_path, "w", "utf-8") as fh:
                fh.write(rendered)
            shutil.copymode(template_path, output_path)
        else:
            logging.info("file is empty")
        print()

    gitmodules = get_gitmodule_list(config)
    for name in gitmodules:
        logging.info("git module \"%s\"" % name)

        url = config["gitmodules"][name]["url"]
        checkout_path = config["gitmodules"][name]["path"]
        total_path = os.path.join(render_dir, checkout_path)

        if os.path.exists(total_path):
            logging.info("remove existing module")
            if not os.path.isdir(total_path):
                logging.critical("git module path is a file")
                raise RuntimeError

            shutil.rmtree(total_path)

        cmd = ["git", "clone", url, checkout_path]
        if "depth" in config["gitmodules"][name]:
            cmd.append("--depth=" + str(config["gitmodules"][name]["depth"]))

        proc = subprocess.Popen(
            cmd, cwd=render_dir, stdout=sys.stdout, stderr=sys.stderr)
        proc.wait()
        if proc.returncode:
            logging.critical("cloning failed")
            raise subprocess.CalledProcessError

        logging.info("complete cloning")
        print()

    if "symlinks" in config:
        for symlink in config["symlinks"]:
            src = os.path.join(render_dir, symlink[0])
            dst = os.path.join(render_dir, symlink[1])
            logging.info("symlink %s -> %s", src, dst)

            if not os.path.exists(src):
                logging.critical("source of symlink does not exist")
                raise RuntimeError

            if os.path.exists(dst):
                logging.info("remove existing symlink")
                if not os.path.islink(dst):
                    logging.critical("destination of symlink is not a symlink")
                    raise RuntimeError
                os.unlink(dst)

            os.link(src, dst)

    exit(0)


def list_configs():
    entries = os.listdir(config_dir)
    for entry in entries:
        path = os.path.join(config_dir, entry)
        if not os.path.isfile(path):
            continue
        if os.path.splitext(path)[1] != ".yml":
            continue
        print(os.path.splitext(entry)[0])
    exit(0)


def list_templates():
    for root, _, files in os.walk(template_dir):
        for file in files:
            print(os.path.relpath(os.path.join(root, file), template_dir))
    exit(0)


def preview():
    render_dir = os.path.join(dotfiles_dir, "rendered")
    if not os.path.exists(render_dir):
        os.makedirs(render_dir)
    render_dotfiles(render_dir, "default")
    exit(0)


def clear_preview():
    render_dir = os.path.join(dotfiles_dir, "rendered")
    if os.path.exists(render_dir):
        logging.info("clear preview \"%s\"", render_dir)
        shutil.rmtree(render_dir)
    exit(0)


parser_main = argparse.ArgumentParser()
subparsers = parser_main.add_subparsers(title="subcommands")

parser_list_configs = subparsers.add_parser("list-configs")
parser_list_configs.set_defaults(func=list_configs)

parser_list_templates = subparsers.add_parser("list-templates")
parser_list_templates.set_defaults(func=list_templates)

parser_preview = subparsers.add_parser("preview")
parser_preview.set_defaults(func=preview)

parser_clear_preview = subparsers.add_parser("clear-preview")
parser_clear_preview.set_defaults(func=clear_preview)

args = parser_main.parse_args()
args.func()