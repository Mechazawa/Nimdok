#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
import json
import Util.irc as ircutil

apiurl = "https://shell-27.appspot.com/shell.do?"
command = ":go"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        msg  = msg[len(command)+1:]
        args = msg.split("|", 2)
        main, imports = msg, ""
        if len(args) == 2:
            imp = []
            for arg in args[0].split(' '):
                if arg.strip('"') != "":
                    imp.append('"%s"' % arg.strip('"'))
            imports = "import(\n    %s\n);\n" % ';\n    '.join(imp)
            main = args[1]

        prog = "package main;\n%sfunc main(){\n    %s;\n}" % (imports, main.lstrip().strip(';'))
        resp = urllib2.urlopen("http://golang.org/compile", "body=%s" % urllib2.quote(prog)).read()
        jo = json.loads(resp)

        result = jo["output"]
        if jo["compile_errors"] != "":
            result = jo["compile_errors"] + "\n\n" + jo["output"]
        result = result.strip()

        if '\n' in resp or '\r' in result:
            paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(prog+"\n\n"+result)).read()
            bot.msg(channel, "%s: %s" % (user, paste))
        elif len(result) > 300:
            bot.msg(channel, ircutil.Trunicate(result ,300))
            paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(prog+"\n\n"+result)).read()
            bot.msg(channel, "%s: %s" % (user, paste))
        else:
            bot.msg(channel, result)


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)