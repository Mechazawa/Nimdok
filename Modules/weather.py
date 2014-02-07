# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *
import urllib2
from xml.dom.minidom import parseString

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
                .replace('<wind_string>','').replace('</wind_string>','') \
                .replace('F', 'f').replace('MPH', 'km/h')

        if location != ', ':
            for i in wind.split():
                try:
                    int(i)
                except:
                    pass
                else:
                    kmph = round(float(i)*1.609, 1)
                    wind = wind.replace(i, str(kmph))

            tempColor = ''
            if '-' in temp:
                tmp = float(temp[1:])
                if tmp >= 0 and tmp < 3:
                    tempColor = stylize.Color.LCyan
                elif tmp >= 3 and tmp < 8:
                    tempColor = stylize.Color.Cyan 
                elif tmp >= 8 and tmp < 15:
                    tempColor = stylize.Color.LBlue 
                elif tmp >= 15:
                    tempColor = stylize.Color.Blue 
            else:
                tmp = float(temp)
                if tmp >= 0 and tmp < 3:
                    tempColor = stylize.Color.White
                elif tmp >= 3 and tmp < 10:
                    tempColor = stylize.Color.Green 
                elif tmp >= 10 and tmp < 25:
                    tempColor = stylize.Color.Yellow 
                elif tmp >= 25 and tmp < 35:
                    tempColor = stylize.Color.Orange 
                elif tmp >= 35:
                    tempColor = stylize.Color.Red 

            bot.msg(channel, user + ': ' + location + ', ' + 
                            stylize.SetColor(temp + 'C', tempColor) + 
                            ', ' + weather + '. Wind blows ' + 
                            wind.strip() + ', ' + humid + ' humidity.')
        else:
            bot.msg(channel, user + ': I couldn\'t find the location.')

@command('w')
def redirect(bot, channel, user, arg):
    parse(bot, channel, user, arg)
