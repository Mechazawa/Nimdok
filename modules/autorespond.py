#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import Util.irc as ircutil

responders = [
    {
        "msg" : "Python is bad",
        "response" : "[USER]: Plz get out"
    } , {
        "msg" : "loli",
        "response" : "pedo"
    } , {
        "msg" : "install gentoo",
        "response" : "install trisquel"
    } , {
        "msg" : "man",
        "response": "What manual page do you want?"
    } , {
        "msg" : "lewd",
        "response": ircutil.Bold("Gigity goo")
    } , {
        "msg" : "rude",
        "response": ircutil.SetColor("NO FIGHTING!", ircutil.Color.Red)
    }
]
def parse(bot, user, channel, msg):
    return
    for resp in responders:
        if msg.strip().lower() == resp["msg"].lower():
            bot.msg(channel, resp["response"].replace("[USER]", user))


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)