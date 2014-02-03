# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *
import random

@handles('msg')
def parse(bot, channel, user, msg):
    if msg.lower().strip().split(' ')[0] == 'nimdok' and msg.lower().replace('nimdok', '').strip() in insults:
        insults = [ 'blows', 'is an ass', 'is broken', 'is crap', 'is shit', 'sucks' ]
        replies = open('insults.in', 'r')
        bot.msg(channel, user+': '+random.choice(replies.readlines()).strip()) 

@command('insult')
def parse(bot, channel, user, msg):
    replies = open('insults.in', 'w')
    replies.write(msg + '\n')
