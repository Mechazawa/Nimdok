#!/usr/bin/env python
# -*- coding: utf-8 -*-

import botlib
import inspect
import events
import modules
import traceback
import thread
import random
import datetime

wait = datetime.datetime.now()

class callback(botlib.callback):
    def __init__(self):
        self.alive = True
        self.cmd = commands()

    def quit(self, bot, user, channel, message):
        print(user+" quit("+message+")")

    def version(self):
        return random.choice([
            "Why are you even requesting this from a bot",
            "You are now breathing manually",
            "You are now aware of your blinking",
            "Microsoft(tm) irc toolkit 1995"
        ])

    def msg(self, bot, user, channel, msg):
        print(user+" in "+channel+": "+msg)
        global wait
        if datetime.datetime.now() < wait or user == "SICPBot":
            return
        for c in events.getEvents('msg'):
            try: 
                #c(bot, user, channel, msg)
                thread.start_new(c, (bot, user, channel, msg,))
            except Exception, e: 
                print e
                print traceback.format_exc()

    def action(self, bot, user, channel, action):
        print(user+" in "+channel+" did "+action)

    def join(self, bot, user, channel):
        print(user+" joined")

#bot essential commands
class commands(botlib.commands):
    def reload(self, bot, user, channel, args):
        if user.lower() != 'bas_': return
        events.clearEvents()
        reload(modules)
        bot.msg(channel, "Reloaded all the modules")

    def shutup(self, bot, user, channel, args):
        if not user.lower() in ["bas_", "lammjohnson", "redlizard", "chown", "naosia", "davexunit"]:
            return
        global wait
        if datetime.datetime.now() < wait:
            bot.msg(channel, "Aready shutting up")
        if args.strip() == "":
            args = "5"
        try:
            t = int(args.strip())
            if t > 15:
                bot.msg(channel, "That's too long")
            else:
                wait = datetime.datetime.now() + datetime.timedelta(minutes=t)
                bot.msg(channel, "Shutting up for %i minutes"%t)
        except:
            bot.msg(channel, "Usage: :shutup {minutes}")

    def speak(self, bot, user, channel, args):
        if not user.lower() in ["bas_", "lammjohnson", "redlizard", "chown", "naosia", "davexunit"]:
            return
        global wait
        wait = datetime.datetime.now()
        bot.msg(channel, "I'm back bitches!")


#datetime.datetime.now()<(datetime.datetime.now() + datetime.timedelta(seconds=3))
#with open('../../botpassword', 'r') as f:
#   nickpass = f.read()

if __name__ == '__main__':
    irc = botlib.connection('irc.rizon.net', 6667, ['#/g/sicp', '#/g/spam'], 'Nimdok', callback(), commands())
    irc.go()

