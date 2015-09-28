from core import Module, on_regex
from re import IGNORECASE


class Bots(Module):
    """
    Basic module that fulfills the requirement that
    it should respond to .bots
    """

    @on_regex(r'^.bots\s*$', flags=IGNORECASE)
    def match_bots(self, bot, channel, *argv):
        bot.message(channel, "[Python] See https://github.com/Mechazawa/Nimdok")
