from BotKit import *
import BotKit.decorators as d

irc = BotKit(
    host = "irc.rizon.net",
    port = 9999,
    ssl = True,

    nickname = "Nimdok_test",

    channels = ["#/g/Spam"],
    verbose=True
)

@d.handles("msg")
def msghandler(bot, channel, user, msg):
    print "#%s %s: %s" % (channel, user, msg)

irc.run()