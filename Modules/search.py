# -*- coding: utf-8 -*-

import urllib2
import json
from HTMLParser import HTMLParser

from BotKit import command, stylize

def unhtml(data):
    return HTMLParser().unescape(data)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

goolink = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='
ddglink = 'https://api.duckduckgo.com/?format=json&pretty=1&no_redirect=1&q='

@command('g')
def parse(bot, channel, user, args):
    try:
        results = json.load(urllib2.urlopen(goolink+urllib2.quote(args)))
        title = stylize.Trunicate(results['responseData']['results'][0]['titleNoFormatting'], 150) \
                .replace('\n', '').replace('\r', '').encode('utf-8')
        content = stylize.Trunicate(results['responseData']['results'][0]['content'], 250) \
                .replace('\n', '').replace('\r', '').encode('utf-8')
        url = results['responseData']['results'][0]['url'].encode('utf-8')
    except:
        noresults = True
    else:
        noresults = False

    if noresults:
        bot.msg(channel, 'No results for ' + args)
    else:
        bot.msg(channel, unhtml(title) + u' · '.encode('utf-8') + url)
        bot.msg(channel, unhtml(strip_tags(content)))

@command('ddg')
def parse(bot, channel, user, args):
    try:
        results = json.load(urllib2.urlopen(ddglink+urllib2.quote(args)))
        definition = stylize.Trunicate(results['Definition'], 150) \
                .replace('\n', '').replace('\r', '').encode('utf-8')
        defisrc = stylize.Trunicate(results['DefinitionSource'], 150) \
                .replace('\n', '').replace('\r', '').encode('utf-8')
        absttext = stylize.Trunicate(results['AbstractText'], 150) \
                .replace('\n', '').replace('\r', '').encode('utf-8')
        abstsource = stylize.Trunicate(results['AbstractSource'], 150) \
                .replace('\n', '').replace('\r', '').encode('utf-8')
        url = results['RelatedTopics'][0]['FirstURL'].encode('utf-8')
    except:
        noresults = True
    else:
        noresults = False

    if noresults:
        bot.msg(channel, 'No results for ' + args)
    else:
        bot.msg(channel, unhtml(definition) + ' (' + defisrc + u') · '.encode('utf-8') + url)
        bot.msg(channel, unhtml(absttext) + ' (' + abstsource + u') · '.encode('utf-8') + url)
