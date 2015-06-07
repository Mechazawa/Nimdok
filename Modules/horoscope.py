"""
I'm a 14 year old girl again!

Mad credits:
https://www.quora.com/What-are-some-free-horoscope-APIs
"""

import requests
from BotKit import command
from BotKit.BotKit.util.stylize import Color, SetColor, Truncate

API_URL = 'http://widgets.fabulously40.com/horoscope.json'
SIGNS = (
    'aries',
    'taurus',
    'gemini',
    'cancer',
    'leo',
    'virgo',
    'libra',
    'scorpio',
    'sagittarius',
    'capricorn',
    'aquarius',
    'pisces',
)

@command('horoscope')
def parse(bot, channel, user, msg):
    sign = msg.strip().lower()

    if not sign:
        bot.msg(channel, SetColor('Usage -- :horoscope {sign}', Color.Orange))
        return

    if sign not in SIGNS:
        bot.msg(channel, SetColor('Unknown Zodiac Sign :c', Color.Red))
        return

    res = requests.get(API_URL, params={'sign': sign})
    jo = res.json()
    horoscope = jo['horoscope']['horoscope']
    qtpi = SetColor(Truncate(horoscope, 240), Color.Green)
    bot.msg(channel, qtpi.encode('utf-8', 'ignore'))
