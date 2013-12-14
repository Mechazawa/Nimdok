#!/usr/bin/python

import botlib, random, re
import sys, sqlite3, os, inspect
import urllib2

#modules
def loadmodules():
    for module in os.listdir('modules'):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__('modules.'+module[:-3], locals(), globals())
    del module

from events import events

class callback(botlib.callback):
    def __init__(self):
        self.alive = True
        self.cmd = commands()

    def quit(self, bot, user, channel, message):
        print user+" quit("+message+")"

    def msg(self, bot, user, channel, msg):
        print user+" in "+channel+": "+msg  
        for c in events['msg']:
            c(bot, user, channel, msg)

    def action(self, bot, user, channel, action):
        print user+" in "+channel+" did "+action

    def join(self, bot, user, channel):
        print user+" joined "+channel

class commands(botlib.commands):
    def help(self, bot, user, channel, args):
        commands = [method[0] for method 
                        in inspect.getmembers(self, predicate=inspect.ismethod) 
                        if method[0][:1] != "_"]
        bot.msg(channel, user + ": " + ', '.join(commands)

    def dongle(self, bot, user, channel, args):
        bot.action(channel, "forks %s's dongle" % user)

    def reload(self, bot, user, channel, args):
        loadmodules()

if __name__ == '__main__':
    dbfile = "botdb.db"
    if not os.path.isfile(dbfile):
        tmpcon = sqlite3.connect(dbfile)
        c = tmpcon.cursor()
        c.execute("CREATE TABLE shouts(id INTEGER PRIMARY KEY, nick VARCHAR, shout VARCHAR);")
        tmpcon.commit()
        c.close()
    database = sqlite3.connect(dbfile)
    settings = botlib.settings('dumbot.db')
    loadmodules()
    irc = botlib.connection('irc.rizon.net', 6667, ['#bottest'], 'Dumbot', callback(), commands(), True)
    irc.go()

