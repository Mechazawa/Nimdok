# -*- coding: utf-8 -*-

import requests
import sqlite3
from bs4 import BeautifulSoup
from BotKit import handles, humanize, stylize, command
from contextlib import closing

def getdomain(s, nosub=False):
    domain = s.split('/')[2].split('?')[0]
    return domain.split('.', domain.count(".")-1)[-1] if nosub else domain


CREATE_DB_QUERY = """
CREATE TABLE IF NOT EXISTS ignored(id INTEGER PRIMARY KEY,
                                  domain VARCHAR UNIQUE)
"""

DB_FILE = 'dbs/urls.db'

ignoreddomains = set()
max_title_length = 250

with sqlite3.connect(DB_FILE) as conn, closing(conn.cursor()) as c:
    c.execute(CREATE_DB_QUERY)
    c.execute("SELECT domain from ignored")
    ignoreddomains = set(map(lambda x: x[0], c))

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
                        bot.msg(channel, stylize.Trunicate(s.replace('\r', ' ').replace('\n', ' '), max_title_length).encode('utf-8'))
                    else: # print the title
                        bot.msg(channel, stylize.Trunicate(title, max_title_length))
                elif 'text' in mime.lower():
                    s = requests.request('GET', m, verify=False).text
                    bot.msg(channel, stylize.Trunicate(s.replace('\r', ' ').replace('\n', ' '), max_title_length).encode('utf-8'))
                else:
                    try:
                        size = int(r.headers['content-length'])
                    except KeyError:
                        size = 0 # can't get content-length for some reason
                    bot.msg(channel, 'Content-Type: ' + str(mime) + ' - ' + humanize.sizefmt(size))

@command('ignoredomain', True)
def addignore(bot, channel, user, args):
    domain = args.split()[0]
    with sqlite3.connect(DB_FILE) as conn, closing(conn.cursor()) as c:
        try:
            c.execute('INSERT INTO ignored(domain) VALUES (?)', (domain,))
            bot.msg(channel, "%s is now ignored" % domain)
        except sqlite3.IntegrityError:
            bot.msg(channel, "%s is already ignored" % domain)
    ignoreddomains.add(domain)

@command('unignoredomain', True)
def addignore(bot, channel, user, args):
    domain = args.split()[0]
    with sqlite3.connect(DB_FILE) as conn, closing(conn.cursor()) as c:
        c.execute('DELETE FROM ignored WHERE domain = ?', (domain,))
        if c.rowcount > 0:
            bot.msg(channel, "%s is no longer ignored" % domain)
            ignoreddomains.remove(domain)
        else:
            bot.msg(channel, "%s wasn't being ignored" % domain)
