# -*- coding: utf-8 -*-

import urllib2
import json
import sqlite3
import os
from re import compile
from BotKit import stylize, command
try:
    from apikeys import lastfm as lastfmkey
except:
    lastfmkey = ''


apiurl = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={APIKEY}&format=json&limit=1"
infourl = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={APIKEY}&format=json&mbid={MBID}'
#collageurl = "http://www.tapmusic.net/lastfm/collage.php?user=%s&type=7day&size=%s&caption=true"
collageurl = "http://nsfcd.com/lastfm/collage.php?user=%s&type=7day&size=%s&caption=true"
dbfile = "dbs/lastfm.db"
xbyx = compile(r"^([1-9]|10)x([1-9]|10)$")

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
            url = apiurl.replace('{APIKEY}', lastfmkey).replace('{USER}', fmuser)
            data = json.load(urllib2.urlopen(url))
            if isinstance(data['recenttracks']['track'], list):
                artist = data['recenttracks']['track'][0]['artist']['#text'].encode('utf-8')
                track = data['recenttracks']['track'][0]['name'].encode('utf-8')
                album = data['recenttracks']['track'][0]['album']['#text'].encode('utf-8')
                np = data['recenttracks']['track'][0]['@attr']['nowplaying']
            else:
                artist = data['recenttracks']['track']['artist']['#text'].encode('utf-8')
                track = data['recenttracks']['track']['name'].encode('utf-8')
                album = data['recenttracks']['track']['album']['#text'].encode('utf-8')
                try:
                    np = data['recenttracks']['track']['@attr']['nowplaying']
                except:
                    np = 'false'
                else:
                    pass
            if 'true' in np:
                state = stylize.SetColor('now playing', stylize.Color.Green)
            else:
                state = stylize.SetColor('last heard', stylize.Color.Red)
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
    elif xbyx.match(s[0].lower()) is not None:
        fmuser = False
        for row in cursor.execute("SELECT lastfm FROM lastfm WHERE nick=?", (user, )):
            fmuser=row[0]
        if not fmuser:
            bot.msg(channel, "%s: I don't know you. Use :np register [lastfm nickname]" % user)
        else:
            url = collageurl % (s[0].lower(), fmuser)
            imgur = urllib2.urlopen("http://imgur.com/upload?url=%s" % url).geturl().split("/")[-1]
            bot.msg(channel, "%s: http://i.imgur.com/%s.jpg" % (user, imgur))

    cursor.close()

#create database
if not os.path.isfile(dbfile):
    tmpcon = sqlite3.connect(dbfile)
    cur = tmpcon.cursor()
    cur.execute("CREATE TABLE lastfm(id INTEGER PRIMARY KEY, nick VARCHAR, lastfm VARCHAR);")
    tmpcon.commit()
    cur.close()

