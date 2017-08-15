import codecs
import importlib
import jinja2
import os
import pkgutil
import yaml


def get_user_dir():
    return os.path.expanduser("~")


def handle_plugins(plugins_config):
    plugin_modules = load_plugins()
    for plugin_name in plugins_config:
        if plugin_name not in plugin_modules:
            raise RuntimeError("cannot find plugin \"{}\"".format(plugin))
        plugin = plugin_modules[plugin_name]
        plugin.handle(plugins_config[plugin_name])


def is_empty_dotfile(text):
    lines = text.splitlines()
    for line in lines:
        if line.strip():
            return False
    return True


def list_configs(path):
    configs = []
    for config in os.listdir(path):
        base, ext = os.path.splitext(path)
        if ext in [".yml", ".yaml"]:
            configs.append(base)
    return configs


def load_plugins():
    import dotgen.plugins as plugins
    plugin_modules = {}
    for info in pkgutil.iter_modules(plugins.__path__):
        plugin_modules[info.name] = importlib.import_module(
            "dotgen.plugins." + info.name)
    return sorted(plugin_modules, key=lambda m: m.rank)


def read_config(path):
    with codecs.open(path, "r", "utf-8") as fh:
        complete_config = yaml.load(fh.read())

    return complete_config["config"], complete_config["plugins"]


def render_templates(template_path, output_path, config):
    loader = jinja2.FileSystemLoader(path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    templates = loader.list_templates()

    for template_name in templates:
        template = env.get_template(template_name)
        content = template.render(config=config)
        if is_empty_dotfile(content):
            continue

        path = os.path.join(output_path, template_name)
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(path, "w") as fh:
            fh.write(content)
