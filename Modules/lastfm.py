#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sqlite3
import os
from xml.dom.minidom import parseString
from BotKit import stylize, command
import apikeys


apiurl="http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={APIKEY}&limit=1"
infourl = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={APIKEY}&mbid={MBID}'
dbfile="dbs/lastfm.db"
@command("np")
def parse(bot, channel, user, msg):
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
              #Courtesy of psycho
              url = urllib2.urlopen(apiurl.replace('{USER}', fmuser).replace('{APIKEY}', apikeys.lastfm)).read()
              data = parseString(url)
              artist = data.getElementsByTagName('artist')[0].toxml() \
                        .rsplit('>')[1].replace('</artist', '') \
                        .replace('&amp;', '&')
              track = data.getElementsByTagName('name')[0].toxml() \
                        .rsplit('>')[1].replace('</name', '') \
                        .replace('&amp;', '&')
              mbid = data.getElementsByTagName('mbid')[0].toxml() \
                        .rsplit('>')[1].replace('</mbid', '')
              try:
                  tinfo = parseString(urllib2.urlopen(infourl.replace('{MBID}', mbid).replace('{APIKEY}', apikeys.lastfm)).read())
              except:
                  pass
              else:
                  genres = []
                  for i in range(2,5):
                       genres.append(tinfo.getElementsByTagName('name')[i].toxml() \
                             .rsplit('>')[1].replace('</name', ''))
                  genre = ''
                  for i in genres:
                      genre += i + ', '
                  album = tinfo.getElementsByTagName('title')[0].toxml() \
                             .rsplit('>')[1].replace('</title', '')

                  state = 'last heard'
                  try:
                      url.index('nowplaying')
                  except:
                      pass
                  else:
                      state = 'now playing'
                  try:
                      album
                  except:
                      bot.msg(channel, stylize.Bold(user) + ' ' + state + ' ' + \
                                        stylize.Bold(stylize.Trunicate(artist, 45)) + ' - ' + \
                                        stylize.Bold(stylize.Trunicate(track, 65)))
                  else:
                      bot.msg(channel, stylize.Bold(user) + ' ' + state + ' ' + \
                                        stylize.Bold(stylize.Trunicate(artist, 45)) + ' - ' + \
                                        stylize.Bold(stylize.Trunicate(track, 65)) + ' (Album: ' + \
                                        album + '; Tags: ' + genre.strip()[:-1] + ')')

    elif s[0].lower() == "register":
        if len(s) != 2:
            bot.msg(channel, "%s: Usage, :np register [last fm nickname]" % user)
        else:
            nick = s[1].strip()
            url = "http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.rss?limit=1&format=txt" % nick
            #print url # what does this do
            try:
                urllib2.urlopen(url).read()
            except:
                raw = 'No user exists with this name.'
            else:
                raw = urllib2.urlopen(url).read()
            if not "No user exists with this name." in raw:
                cursor.execute("DELETE FROM lastfm WHERE nick = ?", (user, ))
                cursor.execute("INSERT INTO lastfm(nick, lastfm) VALUES (?, ?)", (user, nick))
                database.commit()
                bot.msg(channel, "Registered your username. Say :np to show what you're playing")
            else:
                bot.msg(channel, "No user found with the nickname \"%s\"" % nick)
    cursor.close()

#create database 
if not os.path.isfile(dbfile):
    tmpcon = sqlite3.connect(dbfile)
    cur = tmpcon.cursor()
    cur.execute("CREATE TABLE lastfm(id INTEGER PRIMARY KEY, nick VARCHAR, lastfm VARCHAR);")
    tmpcon.commit()
    cur.close()

