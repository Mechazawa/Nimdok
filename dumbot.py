#!/usr/bin/python

import botlib, random, re
import sys, sqlite3, os, inspect
import events
import modules

class callback(botlib.callback):
    def __init__(self):
        self.alive = True
        self.cmd = commands()

    def quit(self, bot, user, channel, message):
        print user+" quit("+message+")"

    def version(self):
        return "Why are you even requesting this from a bot"

    def msg(self, bot, user, channel, msg):
        print user+" in "+channel+": "+msg  
        for c in events.getEvents('msg'):
            c(bot, user, channel, msg)

    def action(self, bot, user, channel, action):
        print user+" in "+channel+" did "+action

    def join(self, bot, user, channel):
        print user+" joined "+channel

#bot essential commands
class commands(botlib.commands):
    def help(self, bot, user, channel, args):
        commands = [method[0] for method  in inspect.getmembers(self, predicate=inspect.ismethod) if method[0][:1] != "_"]
        bot.msg(channel, user + ": " + ', '.join(commands))

    def dongle(self, bot, user, channel, args):
        bot.action(channel, "forks %s's dongle" % user)

    def reload(self, bot, user, channel, args):
        reload(modules)
        bot.msg(channel, "Reloaded all the modules")
        pass

if __name__ == '__main__':
    dbfile = "botdb.db"
    if not os.path.isfile(dbfile):
        tmpcon = sqlite3.connect(dbfile)
        c = tmpcon.cursor()
        c.execute("CREATE TABLE shouts(id INTEGER PRIMARY KEY, nick VARCHAR, shout VARCHAR);")
        tmpcon.commit()
        c.close()
    database = sqlite3.connect(dbfile)
    settings = botlib.settings('users.db')
    irc = botlib.connection('irc.rizon.net', 6667, ['#yolo9000'], 'Dumbot', callback(), commands())
    irc.go()

