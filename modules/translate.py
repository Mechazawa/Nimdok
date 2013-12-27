# -*- coding: utf-8 -*-
#!/usr/bin/python
import events
import urllib2
import urllib
import json


langmap = {
    "afrikaans": "af",
    "albanian": "sq",
    "arabic": "ar",
    "azerbaijani": "az",
    "basque": "eu",
    "bengali": "bn",
    "belarusian": "be",
    "bulgarian": "bg",
    "catalan": "ca",
    "chinese": "zh-cn",
    "chineese": "zh-cn", # I keep typing chineese instead of chinese
    "chinese simplified": "zh-cn",
    "chinese traditional": "zh-tw",
    "simplified chinese": "zh-cn",
    "traditional chinese": "zh-tw",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "filipino": "tl",
    "finnish": "fi",
    "french": "fr",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hebrew": "iw",
    "hindi": "hi",
    "hungarian": "hu",
    "icelandic": "is",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "kannada": "kn",
    "korean": "ko",
    "latin": "la",
    "latvian": "lv",
    "lithuanian": "lt",
    "macedonian": "mk",
    "malay": "ms",
    "maltese": "mt",
    "norwegian": "no",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "romanian": "ro",
    "russian": "ru",
    "serbian": "sr",
    "slovak": "sk",
    "slovenian": "sl",
    "spanish": "es",
    "swahili": "sw",
    "swedish": "sv",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "vietnamese": "vi",
    "welsh": "cy",
    "yiddish": "yi",
}
encodeChars = "$&+,/:;=?@ <>\"'%#{}|\\^~[]`\n\r\t"

command = ":tr"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        msg = msg[4:].decode('utf-8', 'ignore')
        args = {"from" : "auto", "to" : "en"}
        s = msg.split(' ')
        for i in range(0,3,2):
            if len(s) < i+1: continue
            if s[i].lower() in ["from", "to"] and not "\"" in s[i+1] and not "'" in s[i+1]:
                resp = language(s[i+1])
                if not resp:
                    bot.msg(channel, "I do not know how to translate %s %s" % (s[0], s[1]))
                    return
                args[s[i]] = language(s[i+1])
        translateme = msg if len(msg.split(' ')) <= 2 else msg.split(' ', 0 if not s[0] in ["from", "to"] else 2 if len(s) > 2 and not s[2] in ["from", "to"] else 4)[-1]
        if translateme.strip() == "":
            bot.msg(channel, "Nothing to translate :/")
            return
        url = "https://translate.google.com/translate_a/t?"
        #query = ''.join([("%"+hex(ord(c)).split('x')[1]) if c in encodeChars else c for c in translateme]) #FUCK unicode
        query = urllib2.quote(translateme.encode('utf-8', 'ignore'))
        url += urllib.urlencode({
                "client": "a",
                "ie": "UTF-8",
                "oe": "UTF-8",
                "sc": "1",
                "sl": args['from'],
                "tl": args['to'],
                "uptl": args['to']
            }) + "&q=" + query
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0')]
        response = opener.open(url).read()
        if len(response) == 0:
            bot.msg(channel, "No response :<")
        else:
            jo = json.loads(response)["sentences"][0]
            try: bot.msg(channel, jo["trans"].encode("utf-8", "ignore"))
            except:  bot.msg(channel, jo["trans"])



def language(lang):
    lang = lang.lower().strip()
    if lang in langmap:
        return langmap[lang]
    return lang if len([1 for i in langmap if langmap[i] == lang]) > 0 else False

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)