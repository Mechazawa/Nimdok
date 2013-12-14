#!/usr/bin/python

import botlib, random, re
import sys, sqlite3, os, inspect
import urllib2

#modules
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
        #for m in msg.split(' '):
            #if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            #    domain = m.split('/')[2].split('?')[0].lower()
            #    if len(m) > 40:
            #        try:
            #            bot.msg(channel, urllib2.urlopen("http://tinyurl.com/api-create.php?url="+m).read())
            #        except Exception: pass
            #    if 'youtube.' in domain:
            #        bot.msg(channel, modules.youtube.parse(m))
            #    else:
            #        bot.msg(channel, modules.urlinfo.parse(m))

    def action(self, bot, user, channel, action):
        print user+" in "+channel+" did "+action
        if(action.lower() in ['shoots '+bot.nick.lower() ,'murders '+bot.nick.lower(), 'kills '+bot.nick.lower(), 'rapes '+bot.nick.lower()]):
            bot.action(channel, random.choice(['dies', 'faints and falls with his head on something (dead)', 'spontaniously explodes', 'turns into a zombie', 'turns into a ghost']))
        if(action.lower() in ['revives '+bot.nick.lower(), 'goes al frankenstein on '+bot.nick.lower()]):
            bot.msg(channel, 'I\'m back baby!')

    def join(self, bot, user, channel):
        print user+" joined "+channel

class commands(botlib.commands):
    def help(self, bot, user, channel, args):
        commands = [method[0] for method 
                        in inspect.getmembers(self, predicate=inspect.ismethod) 
                        if method[0][:1] != "_"]
        bot.msg(channel, user + ": " + ', '.join(commands))

    def playtest(self, bot, user, channel, args):
        bot.msg(channel,"Please read http://superbossgames.com/wiki/index.php?title=TMC if you want to playtest Intruder.")

    def randint(self, bot, user, channel, args):
        a = self._parseArgs(args)
        a.sort()
        if(len(a) != 2):
            bot.msg(channel, "I need 2 arguments for that command")
        elif(not str(a[0]).replace('-','').isdigit() or not str(a[1]).replace('-','').isdigit()):
            bot.msg(channel, "Both arguments need to be numeric")
        else:
            try: bot.msg(channel, random.randint(a[0],a[1]))
            except Exception, e: bot.msg(channel, str(e))

    def dongle(self, bot, user, channel, args):
        bot.action(channel, "forks %s's dongle" % user)
if __name__ == '__main__':
    dbfile = "botdb.db"
    if not os.path.isfile(dbfile):
        tmpcon = sqlite3.connect(dbfile)
        c = tmpcon.cursor()
        c.execute("CREATE TABLE shouts(id INTEGER PRIMARY KEY, nick VARCHAR, shout VARCHAR);")
        tmpcon.commit()
        c.close()
    database = sqlite3.connect(dbfile)
    settings = botlib.settings('bossbot.db')
    irc = botlib.connection('irc.rizon.net', 6667, ['#bottest'], 'Dumbot', callback(), commands(), True)
    irc.go()

