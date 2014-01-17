#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BotKit import botkit
import events
import Modules
import traceback
import thread
import random
import datetime
import argparse

wait = datetime.datetime.now()

class callback(botkit.callback):
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
            "Microsoft™ irc toolkit 1995",
            "It just werks™ technology"
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
        print(user+" in "+channel+"* "+action)
        global wait
        if datetime.datetime.now() < wait or user == "SICPBot":
            return
        for c in events.getEvents('action'):
            try:
                #c(bot, user, channel, msg)
                thread.start_new(c, (bot, user, channel, action,))
            except Exception, e:
                print e
                print traceback.format_exc()

    def join(self, bot, user, channel):
        print(user+" joined ")
        global wait
        if datetime.datetime.now() < wait or user == "SICPBot":
            return
        for c in events.getEvents('join'):
            try:
                #c(bot, user, channel, msg)
                thread.start_new(c, (bot, user, channel,))
            except Exception, e:
                print e
                print traceback.format_exc()

    def invite(self, bot, user, channel):
        bot.join(channel)

#bot essential commands
class commands(botkit.commands):
    def reload(self, bot, user, channel, args):
        print "Someone called reload"
        if self._ispriv(bot, user):
            events.clearEvents()
            try:
              reload(Modules)
              bot.msg(channel, "Reloaded all the modules")
            except Exception, e:
              print e
              bot.msg(channel, "Something went wrong when I tried to reload my modules :< (did you make a typo somewhere?)")


    def shutup(self, bot, user, channel, args):
        if not self._ispriv(bot, user):
            return
        global wait
        if datetime.datetime.now() < wait:
            bot.msg(channel, "Aready shutting up")
            return
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
        if not self._ispriv(bot, user):
            return
        global wait
        wait = datetime.datetime.now()
        bot.msg(channel, "I'm back bitches!")

    def _ispriv(self, bot, user):
        if user.lower() == 'sicpbot': #nice try faggot
            return False
        who = bot.who(user)
        print "%s [%s]" % (user, who['mode'])
        return len([x for x in "~%&@" if x in who['mode']]) > 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nick',    dest='nick', help='nickname', default='Nimdok')
    parser.add_argument('-s', '--server',  dest='host', help='server',   default='irc.rizon.net')
    parser.add_argument('-p', '--port',    dest='port', help='port',     default=6667, type=int)
    parser.add_argument('-c', '--channel', dest='chan', help='comma sepperated channels', default='#/g/sicp,#/g/spam')
    parser.add_argument(      '--password',dest='passw', help='nick password', default='')
    parser.add_argument('-v', '--verbose', dest='verbose', help='enable verbose mode', action='store_true')

    args = parser.parse_args()
    irc = botkit.connection(args.host, args.port, args.chan.split(','), args.nick, callback(), commands(), password=args.passw, verbose=args.verbose)
    irc.go()

