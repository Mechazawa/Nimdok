from core import Module, on_event


class Echo(Module):

    @on_event('message')
    def pong(self, bot, *argv):
        print("{} {}: {}".format(*argv))
