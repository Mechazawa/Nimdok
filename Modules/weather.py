# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *
import urllib2
import json
try:
    from apikeys import wunder as wunderkey
except:
    wunder = ''

@command('weather')
@command('w')
def parse(bot, channel, user, arg):
    if len(arg) == 0:
        bot.msg(channel, 'Usage, :w <city> [<country>]')
    else:
        location = urllib2.quote(arg)
        apiurl = 'http://api.wunderground.com/api/{APIKEY}/conditions/q/{LOCATION}.json' \
                .replace('{APIKEY}', wunderkey).replace('{LOCATION}', location)
        data = json.load(urllib2.urlopen(apiurl))
        text = urllib2.urlopen(apiurl).read()
        if 'current_observation' in text:
            key = 'current_observation'
            curr_loc = data[key]['display_location']['full']
            weather = data[key]['weather']
            temp = str(data[key]['temp_c']) + u'°C (' + str(data[key]['temp_f']) + u'°F)'
            feel = str(data[key]['feelslike_c']) + u'°C (' + str(data[key]['feelslike_f']) + u'°F)'
            humidity = data[key]['relative_humidity']
            wkph = str(data[key]['wind_kph'])
            wmph = str(data[key]['wind_mph'])
            wind = str(data[key]['wind_string']).replace('MPH', 'km/h').replace(wmph, wkph)
# °
            text = curr_loc + u' · ' + temp + u' · Feels like ' + feel + u' · ' + weather + u' · Humidity: ' + humidity + u' · Wind: ' + wind

            bot.msg(channel, user + ': ' + text.encode('utf-8'))

        elif 'results' in text:
            bot.msg(channel, user + ': there are multiple locations matching "' + arg + '". Try to refine your search.')

        elif 'querynotfound' in text:
            bot.msg(channel, user + ': No location found.')
