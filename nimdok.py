from BotKit import *

irc = BotKit(
    host= "irc.rizon.net",
    port= 9999,
    ssl= True,

    nickname= "Nimdok_test",

    channels= ["#/g/Spam"],
    verbose= True,
    debug= True
)

@handles("msg")
def msghandler(bot, channel, user, msg):
    print "#%s %s: %s" % (channel, user, msg)

@handles("version")
def version(bot, who, args):
    bot.notice(who, "\001VERSION BotKit\001")

@command("ping")
def ping(bot, channel, user, args):
    bot.msg(channel, user+": PONG")

irc.run()