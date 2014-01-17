#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

import events
import BotKit.util.irc as ircutil


command = ":bf"
def parse(bot, user, channel, msg):
    return
    if msg.lower()[:len(command)+1].rstrip() == command:
        msg = msg[len(command)+1:]
        print "[Brainfuck] Found %i bytes of brainfuck" % len(msg)
        try:
            resp = bf(msg, 0, len(msg)-1, "", 0).rstrip()
            if '\n' in resp or '\r' in resp:
                paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(resp)).read()
                bot.msg(channel, "%s: %s" % (user, paste))
            elif len(resp) > 300:
                bot.msg(channel, ircutil.Trunicate(resp ,300))
                paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(resp)).read()
                bot.msg(channel, "%s: %s" % (user, paste))
            else:
                bot.msg(channel, resp)
        except Exception, e:
            print e
            bot.msg(channel, "I know brainfuck is hard... Check your code!")


def bf(src, left, right, data, idx):
    ret = ""
    if len(src) == 0: return
    if left < 0: left = 0
    if left >= len(src): left = len(src) - 1
    if right < 0: right = 0
    if right >= len(src): right = len(src) - 1
    # tuning machine has infinite array size
    # increase or decrease here accordingly
    arr = [0] * 30000
    ptr = 0
    i = left
    while i <= right:
        s = src[i]
        if s == '>':
            ptr += 1
            # wrap if out of range
            if ptr >= len(arr):
                ptr = 0
        elif s == '<':
            ptr -= 1
            # wrap if out of range
            if ptr < 0:
                ptr = len(arr) - 1
        elif s == '+':
            arr[ptr] += 1
        elif s == '-':
            arr[ptr] -= 1
        elif s == '.':
            ret += chr(arr[ptr])
        elif s == ',':
            if idx >= 0 and idx < len(data):
                arr[ptr] = ord(data[idx])
                idx += 1
            else:
                arr[ptr] = 0 # out of input
        elif s =='[':
            if arr[ptr] == 0:
                loop = 1
                while loop > 0:
                    i += 1
                    c = src[i]
                    if c == '[':
                        loop += 1
                    elif c == ']':
                        loop -= 1
        elif s == ']':
            loop = 1
            while loop > 0:
                i -= 1
                c = src[i]
                if c == '[':
                    loop -= 1
                elif c == ']':
                    loop += 1
            i -= 1
        i += 1
    return ret

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)
