#!/usr/bin/env python
# -*- coding: utf-8 -*-
#<Trev>  I don't always Markov chain. But when I do, I'm remarkably relevant life radio can I get an iphone WOOP WOOP

import sqlite3
import os
from datetime import datetime
from BotKit import handles, command
import random
import urllib2

dbfile="dbs/shout.db"
@handles('msg')
def parse(bot, channel, user, msg):
    if msg[0] == ":":
        return #Not even worth doing anything after this if we know someone executed a command
    global lastShout
    if (datetime.now() - lastShout).seconds < random.randint(10,40) or user.lower() == "sicpbot": 
        return
    lastShout = datetime.now()
    ret = ""
    if msg.upper() != msg or len(msg) <= 2 or msg.upper() == msg.lower():
        return
    database = sqlite3.connect(dbfile)
    c = database.cursor()
    shouts = []
    for row in c.execute("SELECT shout from shouts"):
        shouts.append(row[0])
    ret = random.choice(shouts)
    c.execute("INSERT INTO shouts(nick, shout) VALUES (?,?)", (user, msg))
    database.commit()
    c.close()
    if ret:
        bot.msg(channel, ret)

if not os.path.isfile(dbfile):
        tmpcon = sqlite3.connect(dbfile)
        c = tmpcon.cursor()
        c.execute("CREATE TABLE shouts(id INTEGER PRIMARY KEY, nick VARCHAR, shout VARCHAR);")
        tmpcon.commit()
        c.close()

@command('shouts')
def listshouts(bot, channel, user, args):
    database = sqlite3.connect(dbfile)
    c = database.cursor()
    url = urllib2.urlopen("http://nnmm.nl/", '\n'.join([row[0] for row in c.execute("SELECT shout from shouts")])).read()
    bot.msg(channel, "%s: All of my shouts: %s"%(user, url))
    

global lastShout
lastShout = datetime.now()
