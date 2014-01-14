#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randrange
import re
from socket import AF_INET, SOCK_STREAM, socket
from sqlite3 import connect
import inspect
import os


class connection(object):
    def __init__(self, server, port, channels, nick, cb, commands, password="", commandprefix = ":", verbose=False):
        self.server, self.port, self.channels, self.nick, self.callback, self.commands, self.password, self.verbose = server, port, channels, nick, cb, commands, password, verbose #don't judge this line of code plz
        self.commandprefix = commandprefix
        self.r = re.compile('^(?:[:](\S+)!)?(\S+)(?: (?!:)(.+?))(?: (?!:)(.+?))?(?: [:](.+))?$')
        self.running = True


    def _lsend(self, s):
        self.sock.send(s + '\r\n')

    def _lrecv(self):
        c, s = '', ''
        while c != '\n':
            c = self.sock.recv(1)
            if c == '':
                break
            s += c
        line = s.strip('\r\n')
        if(self.verbose):
            print(line)
        return line

    def go(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.server, self.port))

        self._lsend('USER %s 0 0 :bot' % (''.join([chr(randrange(ord('a'), ord('z'))) for i in range(8)])))
        self._lsend('NICK %s 0' % self.nick)

        realNick = self.nick
        # Wait for the 001 status reply.
        while 1:
            line = self._lrecv()
            if(self.verbose):
                print(line)
            if re.compile(':[^ ]+ 001 ').match(line):
                break
            elif 'Nickname is already in use' in line:
                # Change username if taken
                realNick = realNick + '_'
                self._lsend('NICK %s 0' % realNick)
            elif line == '':
                return
                raise 'ConnectError', (self.server, self.port, 'EOFBefore001')

        #identify with the NICKSERV if needed
        if self.password != "" and realNick != self.nick:
            self.msg('NICKSERV', 'GHOST %s %s' % (self.nick, self.password))
            while 1:
                line = self._lrecv().lower()
                if 'has been ghosted' in line:
                    self._lsend('NICK %s 0' % self.nick)
                    break
                elif 'invalid password for' in line:
                    break

        if self.password != "":
            self.msg('nickserv', 'identify %s' % self.password)

        # Join the channels.
        for channel in self.channels:
            self._lsend('JOIN ' + channel)


        while self.running:
            line = self._lrecv()

            if line == '':
                raise 'ConnectionClose', (self.server, self.port)
                return

            elif line[:6] == 'PING :':
                if(self.verbose): print(' PONG :' + line[6:])
                self._lsend('PONG :' + line[6:])
                continue

            try:
                gr = self.r.match(line)
                if(gr.group(1) == self.nick):
                    continue

                elif(gr.group(3) == 'PRIVMSG' and '\001ACTION' in gr.group(5)):
                    self.callback.action(self, gr.group(1), gr.group(4), gr.group(5)[8:][:-1])
                elif(gr.group(3) == 'PRIVMSG'):
                    if gr.group(5) == "\001VERSION\001":
                        self.notice(gr.group(1), self.callback.version() or "SPBL-framework")
                        continue
                    if(gr.group(5)[:1] == self.commandprefix):
                        for method in inspect.getmembers(self.commands, predicate=inspect.ismethod):
                            cmd = method[0]
                            func = method[1]
                            if ((gr.group(5)+' ')[:(len(cmd)+2)] == self.commandprefix+cmd+' ' and cmd[:1] != "_"):
                                func(self, gr.group(1), gr.group(4), gr.group(5)[(len(cmd)+2):])
                    self.callback.msg(self, gr.group(1), gr.group(4), gr.group(5))
                elif(gr.group(3) == 'PART'):
                    self.callback.part(self, gr.group(1), gr.group(4), gr.group(5))
                elif(gr.group(3) == 'JOIN'):
                    self.callback.join(self, gr.group(1), gr.group(4))
                elif(gr.group(3) == 'QUIT'):
                    self.callback.quit(self, gr.group(1), gr.group(4), gr.group(5))
                elif(gr.group(2) == 'NICK'):
                    self.callback.nick(self, gr.group(1), gr.group(3))
                elif(gr.group(3) == 'INVITE'):
                    self.callback.invite(self, gr.group(1), gr.group(5))

                self.callback.raw(self, line)
            except:
                pass

    # Server commands etc
    def msg(self, what, msg):
        #msg = msg.encode("utf-8", "ignore")
        for line in str(msg).replace('\r', '').split('\n'):
            self._lsend('PRIVMSG %s :%s' % (what, line))

    def action(self, what, msg):
        self._lsend('PRIVMSG %s :\001ACTION %s\001' % (what, str(msg)))

    def join(self, channel):
        self._lsend('JOIN ' + channel.replace('\n', ''))

    def part(self, channel, reason=" "):
        self._lsend('PART %s :%s' % (channel, str(reason.replace('\n', ''))))

    def quit(self, reason="Bot shutting down"):
        self._lsend('QUIT :' + str(reason.replace('\n', '')))
        self.running = False

    def nick(self, nick):
        self._lsend('NICK :' + nick.replace('\n', ''))

    def names(self, channel):
        self._lsend('NAMES ' + channel.replace('\n', ''))
        return self._lrecv().split(':')[2].split()

    def notice(self, what, message):
        self._lsend('NOTICE %s :%s' % (what, message))

    def who(self, who):
        self._lsend('WHO %s' % (who.split()[0]))
        resp = ""
        while not "352" in resp:
            resp = self._lrecv()
        match = re.match(':\S+ \d+ \S+ \S+ ~(\S+) (\S+) \* (\S+) (\S+) :\d+ (\S+)', resp)
        return {
            "user" : match.group(1),
            "host" : match.group(2),
            "nick" : match.group(3),
            "mode" : match.group(4),
            "name" : match.group(5)
        }

    def list(self):
        self._lsend('LIST')
        channels = []
        while 1:
            raw = self._lrecv()
            if raw[-13:] == ":End of /LIST":
                break
            raw = raw.replace('\r', '').split('\n')
            for line in raw:
                try:
                    channels.append({"name": line.split(' ')[3],
                                    "users": int(line.split(' ')[4]),
                                    "desc": line.split(':')[2]})
                except:
                    pass
        return channels

    # Info commands
    def getNick(self):
        return self.nick



class callback(object):
    def msg(self, bot, user, channel, msg):
        #print user+" in "+channel+": "+msg
        pass

    def action(self, bot, user, channel, action):
        #print user+" in "+channel+" did "+action
        pass

    def join(self, bot, user, channel):
        #print user+" joined "+channel
        pass

    def version():
        return "SPBL-framework"

    def quit(self, bot, user, channel, message):
        #print user+" joined "+channel
        pass

    def part(self, bot, user, channel, reason):
        #print user+" left "+channel+": "+reason
        pass

    def nick(self, bot, oldnick, newnick):
        #print oldnick+" is now know as "+newnick
        pass

    def invite(self, bot, user, channel):
        pass

    def raw(self, bot, data):
        #print data
        pass


class commands(object):
    def _parseArgs(self, args, parseInt=True):
        c = compile(r"""("[^"]*")|([^\s]+)""").findall(args)
        if parseInt:
            return [int(row[1]) if row[1].replace('-','').isdigit() else row[1] for row in c]
        else:
            return c
