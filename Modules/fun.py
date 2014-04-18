# -*- coding: utf-8 -*-
from BotKit import handles, command
import random


@command('8ball')
def parse(bot, channel, user, msg):
    if len(msg) == 0:
        bot.msg(channel, 'Usage: :8ball <question>')
    else:
        answers = ['yes', 'no', 'without a doubt', 'as i see it, yes', 'ask me again later',
                   'don\'t count on it', 'my sources say no', 'very doubtful', 'don\'t care, go away']
        bot.msg(channel, user + ': ' + random.choice(answers) + '.')


@handles('msg')
def parse(bot, channel, user, msg):
    answers = ['yes', 'no']
    if 'y/n' in msg.split():
        bot.msg(channel, user + ': ' + random.choice(answers) + '.')

