# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *
import random

filename = 'insults.in' 
insults = [ 'blows', 'is an ass', 'is broken', 'is crap', 'is shit', 'sucks' ]

@handles('msg')
def parse(bot, channel, user, msg):
    if msg.lower().strip().split(' ')[0] == 'nimdok' and msg.lower().replace('nimdok', '').strip() in insults:
        replies = open(filename, 'r')
        bot.msg(channel, user+': '+random.choice(replies.readlines()).strip())

@command('insult')
def parse(bot, channel, user, msg):
    replies = open(filename, 'w')
    replies.write(msg + '\n')
    bot.msg(channel, 'Insult added.')
