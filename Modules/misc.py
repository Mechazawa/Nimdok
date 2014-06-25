# -*- coding: utf-8 -*-
from BotKit import command, handles

@command("dongle")
def fork(bot, channel, user, arg):
    forkable = arg.split()[0] if len(arg.split()) else user
    bot.action(channel, "forks %s'%s dongle" % (forkable, "s" if forkable[-1].lower() not in "zxs" else ""))

@handles("msg")
def dongers(bot, channel, user, msg):
    if "donger" in msg.lower():
        bot.msg(channel, u"ヽ༼ຈل͜ຈ༽ﾉ raise ur dongers ヽ༼ຈل͜ຈ༽ﾉ".encode("utf-8", "ignore"))

@command("helix")
def consult(bot, channel, user, msg):
    bot.msg(channel ,"This isn't the time for that %s!" % user.upper())

@command("ping") def parse(bot, channel, user, arg):
    bot.msg(channel, user+": pong")
