from BotKit import *
import Modules

irc = BotKit(
    host= "irc.rizon.net",
    port= 9999,
    ssl= True,

    nickname= "Nimdok_test",

    channels= ["#/g/Spam"],
    verbose= True,
    debug= True
)

irc.run()