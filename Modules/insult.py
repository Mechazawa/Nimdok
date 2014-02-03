# -*- coding: utf-8 -*-
#!/usr/bin/python
# Made by psycho

from BotKit import handles
import random

replies = [ 'no u', 'your mother is so fat, the recursive function computing her mass causes a stack overflow' ]
insults = [ 'blows', 'is an ass', 'is broken', 'is crap', 'is shit', 'sucks' ]

@handles('msg')
def parse(bot, channel, user, msg):
    if msg.lower().strip().split(' ')[0] == 'nimdok' and msg.lower().replace('nimdok', '').strip() in insults:
        bot.msg(channel, user+': '+random.choice(replies)) 
