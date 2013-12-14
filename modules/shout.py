import sqlite3
from events import events 

database = sqlite3.connect("botdb.db")

def parse(bot, user, channel, msg):
    ret = ""
    if msg.upper() != msg: return ret
    c = database.cursor()
    for row in c.execute("SELECT shout from shouts ORDER BY RANDOM() LIMIT 1"):
        ret = channel, row[0]
    c.execute("INSERT INTO shouts(nick, shout) VALUES (?,?)", (user, msg))
    database.commit()
    c.close()
    if ret:
        bot.msg(channel, ret)

events['msg'].append(parse)
print "Shout module loaded"