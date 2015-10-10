from core import Module, on_event


class Log(Module):

    @on_event('message')
    def on_chat(self, bot, channel, user, message):
        bot.logger.info("{} {}: {}".format(channel, user, message))
