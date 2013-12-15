import sqlite3
import events

database = sqlite3.connect("botdb.db")

def parse(bot, user, channel, msg):
    ret = ""
    if msg.upper() != msg or len(msg) <= 4 or msg.upper() == msg.lower() : return ret
    c = database.cursor()
    for row in c.execute("SELECT shout from shouts ORDER BY RANDOM() LIMIT 1"):
        ret = row[0]
    c.execute("INSERT INTO shouts(nick, shout) VALUES (?,?)", (user, msg))
    database.commit()
    c.close()
    if ret:
        bot.msg(channel, "\0034"+ret)

events.setEvent('msg', 'shout', parse)
print "Shout module loaded"