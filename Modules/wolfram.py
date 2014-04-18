# -*- coding: utf-8 -*-

import urllib2
import lxml.etree as et
from BotKit import command, stylize
try:
  from apikeys import wolframalpha as wolframalphakey
except:
  wolframalphakey = ''

apiurl="http://api.wolframalpha.com/v2/query?"
#set params
apiurl+="units=metric&location=Amsterdam&reinterpret=true&format=plaintext&excludepodid=Input&"
@command("wa")
def parse(bot, channel, user, msg):
  #build url
  url = apiurl + "appid=" + wolframalphakey
  url += "&input=" + urllib2.quote(msg)

  #get result
  raw = urllib2.urlopen(url).read()
  tree = et.fromstring(raw)

  #parse result
  if tree.get('error') != 'false':
    bot.msg(channel, "Wolfram alpha returned an error")
  elif tree.get('numpods') > 0:
    result = tree.find('pod').find('subpod').find('plaintext').text
    result = result.encode('UTF-8', 'ignore') #fucking unicode
    bot.msg(channel, "%s: %s" % (user, stylize.Trunicate(result.split('\n')[0] ,300)))
  elif len(tree.findall('tips')) > 0:
      bot.msg(channel, "%s: %s" % (user, tree.find('tips').find('tip').get('text')))
  else:
      bot.msg(channel, "%s: I didn't find what you were looking for" % user)
