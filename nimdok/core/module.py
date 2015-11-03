from re import compile
from .util import parametrized
import inspect


class Module(object):
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.bot = bot

    def get_hooks(self):
        return [member for member in inspect.getmembers(self)
                if isinstance(member, HookWrapper)]


class HookWrapper(object):
    """
    This will hook into `on_none` something that will
    never be called.
    """
    hook_type = 'none'

    def __init__(self, method):
        self.method = method

    def __call__(self, *argv, **kwargs):
        self.method(*argv, **kwargs)


class CommandHook(HookWrapper):
    hook_type = 'message'
    command_prefix = ':'

    def __init__(self, method, command):
        self.command = command.lower()
        super().__init__(method)

    def __call__(self, oself, bot, source, target, message):
        if message[0] != self.command_prefix:
            return

        command = self.command_prefix + self.command
        start, end = message[:len(command)], message[len(command):]

        if start.lower() == command and (end == '' or end[0] == ' '):
            return self.method(oself, bot, source, target, message[1])


@parametrized
def on_command(method, command):
    return CommandHook(method, command)


class RegexHook(HookWrapper):
    hook_type = 'message'

    def __init__(self, method, regex, flags=0):
        self.regex = compile(regex, flags)
        super().__init__(method)

    def __call__(self, oself, bot, source, target, message):
        match = self.regex.match(message)
        if match is not None:
            return self.method(oself, bot, source, target, message, match)


@parametrized
def on_regex(method, regex, flags=0):
    return RegexHook(method, regex, flags)


class EventHook(HookWrapper):
    hook_type = 'none'

    def __init__(self, method, hook_type):
        super().__init__(method)
        self.hook_type = hook_type


@parametrized
def on_event(method, hook_type='message'):
    return EventHook(method, hook_type)
