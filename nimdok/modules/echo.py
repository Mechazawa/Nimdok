from core import Module, on_event


class Echo(Module):

    @on_event('message')
    def pong(self, bot, source, target, message):
        print("{} {}: {}".format(target, source, message))
