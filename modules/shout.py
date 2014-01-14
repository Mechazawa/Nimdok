#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import events
import os
from datetime import datetime, time
import random

dbfile="dbs/shout.db"
def parse(bot, user, channel, msg):
    if msg[0] == ":":
        return #Not even worth doing anything after this if we know someone executed a command
    global lastShout
    if (datetime.now() - lastShout).seconds < random.randint(10,40) or user.lower() == "sicpbot": 
        return
    lastShout = datetime.now()
    database = sqlite3.connect(dbfile)
    ret = ""
    if msg.upper() != msg or len(msg) <= 2 or msg.upper() == msg.lower():
        return
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

lastShout = datetime.now()
events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)
