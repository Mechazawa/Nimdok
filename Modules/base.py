# -*- coding: utf-8 -*-

import re


class BaseModule(object):
    _module_regex = re.compile(r"/?([\w\-_]+)\.pyc?")

    def __init__(self, file_name):
        module_match = BaseModule._module_regex.match(file_name)
        assert module_match is not None

        self.module = module_match.group(1)
        self.commands = []
        self.events = []

    def command(self, name, restricted=False, bypass_ignore=False):
        """
        Decorator to add a command

        @type name: str
        @param name: The command name. This is how the command will be called
        @type restricted: bool
        @param restricted: if this is an admin-only command
        @return: decorator
        """
        def decorator(f):
            self.commands.append(IrcCommand(name, f, restricted, bypass_ignore))
        return decorator


class IrcCommand(object):
    def __init__(self, name, method, restricted, bypass_ignore):
        self.name = name
        self.method = method
        self.restricted = restricted
        self.bypass_ignore = bypass_ignore
