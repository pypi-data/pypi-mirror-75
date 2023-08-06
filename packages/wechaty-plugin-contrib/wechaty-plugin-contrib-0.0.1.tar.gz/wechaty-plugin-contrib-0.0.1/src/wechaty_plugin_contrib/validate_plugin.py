"""
plugin validator
"""
from __future__ import annotations
from wechaty import WechatyPlugin


def validate_plugin(plugin: WechatyPlugin):
    """validate the plugin"""
    # check the name of the plugin
    if type(plugin) is WechatyPlugin:
        raise Exception('plugin instance should a subclass of WechatyPlugin')

    # check the name of plugin
    if not hasattr(plugin, 'name'):
        raise Exception('WechatyPlugin must have name property')

    class_name = type(plugin).__name__
    if not class_name.endswith('Plugin'):
        raise Exception('the name of plugin <%s> should follow the Rule: '
                        'NamePlugin' % class_name)
