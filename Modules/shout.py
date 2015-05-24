# -*- coding: utf-8 -*-
# <Trev>  I don't always Markov chain. But when I do, I'm remarkably relevant
#         life radio can I get an iphone WOOP WOOP

import sqlite3
from datetime import datetime
from BotKit import handles, command
from random import randint
import requests
from contextlib import closing

CREATE_DB_QUERY = """
CREATE TABLE IF NOT EXISTS shouts(id INTEGER PRIMARY KEY,
                                  nick VARCHAR,
                                  shout VARCHAR)
"""

DB_FILE = 'dbs/shout.db'


@handles('msg')
def parse(bot, channel, user, msg):
    global last_shout
    msg = msg.decode('utf-8', 'ignore')

    if msg.startswith(':'):
        return  # Ignore prefixed commands.
    try:
        if (datetime.now() - last_shout).seconds < randint(10, 40):
            return
    except NameError:
        pass
    if user.lower() == 'sicpbot':
        return  # Ignore sicpbot.
    if not is_shout(msg):
        return

    last_shout = datetime.now()

    with sqlite3.connect(DB_FILE) as conn, closing(conn.cursor()) as c:
        c.execute(CREATE_DB_QUERY)

        c.execute('SELECT shout FROM shouts ORDER BY RANDOM() LIMIT 1;')
        row = c.fetchone()
        if row:
            bot.msg(channel, row[0].encode('utf-8', 'ignore'))

        c.execute('INSERT INTO shouts(nick, shout) VALUES (?,?)',
                  (user, msg))


@command('shouts')
def listshouts(bot, channel, user, args):
    with sqlite3.connect(DB_FILE) as conn, closing(conn.cursor()) as c:
        c.execute(CREATE_DB_QUERY)

        c.execute('SELECT shout FROM shouts')
        shouts = '\n'.join(row[0] for row in c).encode('utf-8', 'ignore')

    url = requests.post(
        'https://nnmm.nl/',
        shouts,
    ).text

    bot.msg(channel, '{}: All of my shouts: {}'.format(user, url))


def is_shout(s):
    """Validate shout

    Must meet the following criteria:
    1. Is all upper case.
    2. must be at least 4 letters long.
    3. At least half of the letters not symbols.
    """
    return (s.upper() == s and
            len(s) >= 4 and
            sum(1 for c in s if c.isupper()) >= len(s)/2)
