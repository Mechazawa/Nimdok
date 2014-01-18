from BotKit import *
import Modules
import apikeys

irc = BotKit(
    host= "irc.rizon.net",
    port= 9999,
    ssl= True,

    nickname= "Nimdok",
    nickpass=apikeys.botpass,

    channels= ["#/g/Spam"],
    debug= True
)

#general bot stuff
@handles('invite')
def invite(bot, channel, user):
    bot.logger.info("Invited to #%s" % channel)
    bot.join(channel)

irc.run()