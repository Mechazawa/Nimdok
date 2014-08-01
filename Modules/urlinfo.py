# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from BotKit import handles, humanize, stylize

def getdomain(s, nosub=False):
    domain = s.split('/')[2].split('?')[0]
    return domain.split('.', domain.count(".")-1)[-1] if nosub else domain

ignoreddomains = ["youtube.com", "youtu.be", "4chan.org", "twitter.com"]

@handles('msg')
def parse(bot, channel, user, msg):
    for m in msg.split(' '):
        if m[:4] == 'http' and '//' in m[5:-len(m)+8]:
            if getdomain(m, True) in ignoreddomains:
                continue
            try:
                r = requests.request('HEAD', m, verify=False)
            except requests.exceptions.ConnectionError: # inexistent websites or issues like `Max retries exceeded'
                #bot.msg(channel, 'A connection error occured.')
                pass
            except requests.exceptions.HTTPError:
                #bot.msg(channel, 'An HTTP error occured.')
                pass
            except requests.exceptions.TooManyRedirects:
                #bot.msg(channel, 'Too many redirects.')
                pass
            else:
                mime = r.headers['content-type']
                if 'html' in mime.lower():
                    s = requests.request('GET', m, verify=False).text
                    BS = BeautifulSoup(s)
                    try: # for websites without a title, as sprunge, so they won't spit out an AttributeError
                        title = BS.find('title').text.replace('\r', ' ').replace('\n', ' ').strip().encode('utf-8')
                    except: # just print the same as if it were a text/plain
                        bot.msg(channel, stylize.Trunicate(s.replace('\r', ' ').replace('\n', ' ')).encode('utf-8'))
                    else: # print the title
                        bot.msg(channel, stylize.Trunicate(title))
                elif 'text' in mime.lower():
                    s = requests.request('GET', m, verify=False).text
                    bot.msg(channel, stylize.Trunicate(s.replace('\r', ' ').replace('\n', ' ')).encode('utf-8'))
                else:
                    try:
                        size = int(r.headers['content-length'])
                    except KeyError:
                        size = 0 # can't get content-length for some reason
                    bot.msg(channel, 'Content-Type: ' + str(mime) + ' - ' + humanize.sizefmt(size))
