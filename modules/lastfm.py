#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
import Util.irc as ircutil
import sqlite3
import os


apiurl="http://ws.audioscrobbler.com/1.0/user/{USER}/recenttracks.rss?limit=1&format=txt"
dbfile="dbs/lastfm.db"
command=":np"
def parse(bot, user, channel, msg):
  if msg.lower()[:len(command)+1].rstrip() == command:
    msg = msg[len(command)+1:].strip()
    s = msg.split()
    database = sqlite3.connect(dbfile)
    cursor = database.cursor()
    if len(s) == 0:
          fmuser = False
          for row in cursor.execute("SELECT lastfm FROM lastfm WHERE nick=?", (user, )):
              fmuser=row[0]
          if not fmuser:
              bot.msg(channel, "%s: I don't know you. Use :np register [lastfm nickname]" % user)
          else:
              playing = getplaying(fmuser).strip().replace('\n', ' ').replace('\r' ,'')
              bot.msg(channel, ircutil.Bold(user) + " is now playing " + ircutil.Bold(playing).strip())
            
    elif s[0].lower() == "register":
        if len(s) != 2:
            bot.msg(channel, "%s: Usage, :np register [last fm nickname]" % user)
        else:
            nick = s[1]
            if getplaying(nick):
                cursor.execute("DELETE FROM lastfm WHERE nick = ?", (user, ))
                cursor.execute("INSERT INTO lastfm(nick, lastfm) VALUES (?, ?)", (user, nick))
                database.commit()
                bot.msg(channel, "Registered your username. Say :np to show what you're playing")
            else:
                bot.msg(channel, "No user found with the nickname \"%s\"" % nick)
    cursor.close()
            
def getplaying(user):
    try:
      raw = urllib2.urlopen(apiurl.replace("{USER}", user)).read()
      if "No user exists with this name." in raw:
          return False
      else:
          return raw.split(',', 2)[1]
    except Exception, e:
        print e
        return False


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)

#create database 
if not os.path.isfile(dbfile):
    tmpcon = sqlite3.connect(dbfile)
    cur = tmpcon.cursor()
    c.execute("CREATE TABLE lastfm(id INTEGER PRIMARY KEY, nick VARCHAR, lastfm VARCHAR);")
    tmpcon.commit()
    c.close()

