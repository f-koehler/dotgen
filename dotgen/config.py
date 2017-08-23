# -*- coding: utf-8 -*-
import codecs
import jinja2
import os
import yaml


def get_default_config_dir():
    return os.path.join(get_home_dir(), ".dotfiles", "configs")


def get_default_template_dir():
    return os.path.join(get_home_dir(), ".dotfiles", "templates")


def get_home_dir():
    return os.path.expanduser("~")


def is_empty_dotfile(text):
    lines = text.splitlines()
    for line in lines:
        if line.strip():
            return False
    return True


def list_configs(path):
    configs = []
    for config in os.listdir(path):
        base, ext = os.path.splitext(config)
        if ext == ".yml":
            configs.append(base)
    return configs


def list_templates(path):
    loader = jinja2.FileSystemLoader(path)
    templates = loader.list_templates()
    return templates


def read_config(path):
    with codecs.open(path, "r", "utf-8") as fh:
        complete_config = yaml.load(fh.read())

    return complete_config["config"], complete_config["plugins"]


def render_dotfiles(template_path, config):
    loader = jinja2.FileSystemLoader(template_path)
    env = jinja2.Environment(
        loader=loader,
        block_start_string="@{%",
        block_end_string="%}@",
        variable_start_string="@{{",
        variable_end_string="}}@",
        comment_start_string="@{#",
        comment_end_string="#}@",
        trim_blocks=True)
    templates = loader.list_templates()

    dotfiles = {}

    for template_name in templates:
        template = env.get_template(template_name)
        content = template.render(config=config)
        if is_empty_dotfile(content):
            continue

        dotfiles[template_name] = content

    return dotfiles
