# -*- coding: utf-8 -*-
#!/usr/bin/python
from random import randrange
from re import compile
from socket import AF_INET, SOCK_STREAM, socket
from sqlite3 import connect
import inspect
import os


class connection(object):
    def __init__(self, server, port, channels, nick, cb, commands, password="", channelpasswd="", verbose=False):
        self.server, self.port, self.channels, self.nick, self.callback, self.commands, self.password, self.verbose = server, port, channels, nick, cb, commands, password, verbose
        self.r = compile('^(?:[:](\S+)!)?(\S+)(?: (?!:)(.+?))(?: (?!:)(.+?))?(?: [:](.+))?$')
        self.running = True

    def lsend(self, s):
        self.sock.send(s + '\r\n')

    def lrecv(self):
        c, s = '', ''
        while c != '\n':
            c = self.sock.recv(1)
            if c == '': # connection closed
                break
            s += c
        line = s.strip('\r\n')
        if(self.verbose):
            print(line)
        return line

    def go(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.server, self.port))

        self.lsend('USER %s 0 0 :bot' % (''.join([chr(randrange(ord('a'),
                                                ord('z'))) for i in range(8)])))
        self.lsend('NICK %s 0' % self.nick)

        realNick = self.nick
        # Wait for the 001 status reply.
        while 1:
            line = self.lrecv()
            if(self.verbose):
                print(line)
            if compile(':[^ ]+ 001 ').match(line):
                break
            elif 'Nickname is already in use' in line:
                # Change username if taken
                realNick = realNick + '_'
                self.lsend('NICK %s 0' % realNick)
            elif line == '':
                raise 'ConnectError', (self.server, self.port, 'EOFBefore001')

        #identify with the NICKSERV if needed
        if self.password != "" and realNick != self.nick:
            self.msg('NICKSERV', 'GHOST %s %s' % (self.nick, self.password))
            while 1:
                line = self.lrecv().lower()
                if 'has been ghosted' in line:
                    self.lsend('NICK %s 0' % self.nick)
                    break
                elif 'invalid password for' in line:
                    break
        if self.password != "":
            self.msg('NICKSERV', 'IDENTIFY %s' % self.password)

        # Join the channels.
        for channel in self.channels:
            self.lsend('JOIN ' + channel)

        while self.running:
            line = self.lrecv()

            if line == '':
                raise 'ConnectionClose', (self.server, self.port)

            elif line[:6] == 'PING :':
                if(self.verbose): print ' PONG :' + line[6:]
                self.lsend('PONG :' + line[6:])
                continue

            gr = self.r.match(line)
            if(gr.group(1) == self.nick):
                continue

            elif(gr.group(3) == 'PRIVMSG' and '\001ACTION' in gr.group(5)):
                self.callback.action(self, gr.group(1), gr.group(4), gr.group(5)[8:][:-1])
            elif(gr.group(3) == 'PRIVMSG'):
                if(gr.group(5)[:1] == "!"):
                    for method in inspect.getmembers(self.commands, predicate=inspect.ismethod):
                        cmd = method[0]
                        func = method[1]
                        if ((gr.group(5)+' ')[:(len(cmd)+2)] == "!"+cmd+' ' and cmd[:1] != "_"):
                            func(self, gr.group(1), gr.group(4), gr.group(5)[(len(cmd)+2):])
                elif gr.group(5) == "\001VERSION\001":
                    self.lsend('NOTICE %s :\001VERSION %s\001' % (gr.group(1), self.callback.version()))
                else:
                    self.callback.msg(self, gr.group(1), gr.group(4), gr.group(5))
            elif(gr.group(3) == 'PART'):
                self.callback.part(self, gr.group(1), gr.group(4), gr.group(5))
            elif(gr.group(3) == 'JOIN'):
                self.callback.join(self, gr.group(1), gr.group(4))
            elif(gr.group(3) == 'QUIT'):
                self.callback.quit(self, gr.group(1), gr.group(4), gr.group(5))
            elif(gr.group(2) == 'NICK'):
                self.callback.nick(self, gr.group(1), gr.group(3))

            self.callback.raw(self, line)

    def msg(self, what, msg):
        for line in str(msg).replace('\r', '').split('\n'):
            self.lsend('PRIVMSG %s :%s' % (what, line))

    def action(self, what, msg):
        self.lsend('PRIVMSG %s :\001ACTION %s\001' % (what, str(msg)))

    def join(self, channel):
        self.lsend('JOIN ' + channel.replace('\n', ''))

    def part(self, channel, reason=" "):
        self.lsend('PART %s :%s' % (channel, str(reason.replace('\n', ''))))
        self.running = False

    def quit(self, reason="Bot shutting down"):
        self.lsend('QUIT :' + str(reason.replace('\n', '')))
        self.running = False

    def nick(self, nick):
        self.lsend('NICK :' + nick.replace('\n', ''))

    def names(self, channel):
        self.lsend('NAMES ' + channel.replace('\n', ''))
        return self.lrecv().split(':')[2].split()

    def list(self):
        self.lsend('LIST')
        channels = []
        while 1:
            raw = self.lrecv()
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


class settings(object):
    def __init__(self, filename):
        if not os.path.isfile(filename):
            tmpcon = connect(filename)
            print "Database file not found. Creating one..."
            c = tmpcon.cursor()
            c.execute("CREATE TABLE prefs(nick VARCHAR, setting VARCHAR, value VARCHAR, PRIMARY KEY(nick, setting));")
            tmpcon.commit()
            c.close()
            print "Done"
        self.conn = connect(filename)

    def get(self, nick, pref, default):
        c = self.conn.cursor()
        for row in c.execute("SELECT value FROM prefs WHERE nick = ? AND setting = ?", (nick, pref)):
            c.close()
            return int(row[0]) if row[0].replace('-','').isdigit() else row[0]
        c.execute("INSERT INTO prefs (nick, setting, value) VALUES (?,?,?)", (nick, pref, default))
        self.conn.commit()
        c.close()
        return default

    def set(self, nick, pref, value):
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO prefs (nick, setting, value) VALUES (?,?,?)", (nick, pref, str(value)))
        self.conn.commit()
        c.close()