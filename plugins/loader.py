"""
    plugin routes in format:
        {
            "url": "some/url",
            "handler": some_function
        }
"""
import os
import importlib.util

# TODO: to json configs

PLUGIN_DIRECTORY = '.'

def is_plugin_directory(file_name):
    return file_name.endswith("_plugin")


def is_route_file_name(file_name):
    return file_name == "routes.py"


def is_protocol_file_name(file_name):
    return file_name == "protocol.py"


def is_factory_file_name(file_name):
    return file_name == "factory.py"


def import_component(component_name, file_path):
    spec = importlib.util.spec_from_file_location('module', file_path)
    component = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(component)
    return getattr(component, component_name)


PLUGIN_PROTOCOL_NAME = 'PluginProtocol'
PLUGIN_FACTORY_NAME = 'PluginFactory'
PLUGIN_ROUTES_NAME = 'plugin_routes'

plugin_routes = []
plugin_protocols = []
plugin_factories = []


def get_plugin_components():
    try:
        directory_listing = os.listdir(PLUGIN_DIRECTORY)
        for dir_name in directory_listing:
            if os.path.isdir(dir_name) and is_plugin_directory(dir_name):
                # TODO: normal path
                plugin_dir_listing = os.listdir(PLUGIN_DIRECTORY + '/' + dir_name)
                for file_name in plugin_dir_listing:
                    file_path = PLUGIN_DIRECTORY + '/' + dir_name + '/' + file_name
                    if is_route_file_name(file_name):
                        plugin_routes.append(import_component(PLUGIN_ROUTES_NAME, file_path))
                    elif is_factory_file_name(file_name):
                        plugin_factories.append(import_component(PLUGIN_FACTORY_NAME, file_path))
                    elif is_protocol_file_name(file_name):
                        plugin_protocols.append(import_component(PLUGIN_PROTOCOL_NAME, file_path))

    except WindowsError as win_err:
        print('Directory error: ', str(win_err))