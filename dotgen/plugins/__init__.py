# -*- coding: utf-8 -*-
from colorama import Fore
import importlib
import pkgutil


def handle_plugins(output_dir, plugins_config):
    plugin_cfgs = []
    for plugin_name in plugins_config:
        mod = importlib.import_module("dotgen.plugins." + plugin_name)
        rank = mod.rank
        config = plugins_config[plugin_name]
        plugin_cfgs.append({
            "name": plugin_name,
            "module": mod,
            "rank": rank,
            "config": config
        })

    plugin_cfgs.sort(key=lambda cfg: cfg["rank"])

    for cfg in plugin_cfgs:
        print(Fore.BLUE + "plugin: " + cfg["name"] + Fore.RESET)
        cfg["module"].handle(output_dir, cfg["config"])
        print(Fore.BLUE + "done\n" + Fore.RESET)
