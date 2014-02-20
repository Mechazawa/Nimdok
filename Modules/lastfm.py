#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import sqlite3
import os
from BotKit import stylize, command
import apikeys


apiurl="http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={APIKEY}&format=json&limit=1"
infourl = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={APIKEY}&format=json&mbid={MBID}'
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
            url = apiurl.replace('{APIKEY}', apikeys.lastfm).replace('{USER}', fmuser)
            data = json.load(urllib2.urlopen(url))
            try:
                artist = data['recenttracks']['track'][0]['artist']['#text']
            except:
                artist = data['recenttracks']['track']['artist']['#text']
            else:
                pass
            try:
                track = data['recenttracks']['track'][0]['name']
            except:
                track = data['recenttracks']['track']['name']
            else:
                pass
            try:
                album = data['recenttracks']['track'][0]['album']['#text']
            except:
                album = data['recenttracks']['track']['album']['#text']
            else:
                pass
            state = stylize.SetColor('last heard', stylize.Color.Red)
            try:
                data.index('nowplaying')
            except:
                pass
            else:
                state = stylize.SetColor('now playing', stylize.Color.Green)
            if album != '':
                bot.msg(channel, stylize.Bold(user) + ' ' + state + ' ' + \
                                 stylize.Bold(stylize.Trunicate(artist, 45)) + ' - ' + \
                                 stylize.Bold(stylize.Trunicate(track, 65)) + ' (Album: ' + \
                                 album + ')')
            else:
                bot.msg(channel, stylize.Bold(user) + ' ' + state + ' ' + \
                                 stylize.Bold(stylize.Trunicate(artist, 45)) + ' - ' + \
                                 stylize.Bold(stylize.Trunicate(track, 65)))
             
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

