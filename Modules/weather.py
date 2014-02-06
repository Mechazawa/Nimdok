# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *
import urllib2
from xml.dom.minidom import parseString

@command('w')
def redirect(*args):
    parse(*args)

@command('weather')
def parse(bot, channel, user, arg):
    if len(arg) == 0:
        bot.msg(channel, 'Usage: :weather <city> [<country>]')
    else:
        try:
            arg.split(' ')[1]
        except:
            loc = arg.split(' ')[0]
        else:
            loc = arg.split(' ')[0] + ',' + arg.split(' ')[1]

        url = 'http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query='+loc.strip()
        data = parseString(urllib2.urlopen(url).read())

        location = data.getElementsByTagName('full')[0].toxml() \
                .replace('<full>','').replace('</full>','')
        temp = data.getElementsByTagName('temp_c')[0].toxml() \
                .replace('<temp_c>','').replace('</temp_c>','')
        weather = data.getElementsByTagName('weather')[0].toxml() \
                .replace('<weather>','').replace('</weather>','')
        humid = data.getElementsByTagName('relative_humidity')[0].toxml() \
                .replace('<relative_humidity>','').replace('</relative_humidity>','')
        wind = data.getElementsByTagName('wind_string')[0].toxml() \
                .replace('<wind_string>','').replace('</wind_string>','')

        if location != ', ':
            bot.msg(channel, user + ': ' + location + ', ' + temp + 'C. Wind blows ' + wind.lower() + ', ' + humid + ' humidity.')
        else:
            bot.msg(channel, user + ': I couldn\'t find the location.')
