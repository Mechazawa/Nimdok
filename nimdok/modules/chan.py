from core import Module, on_regex, IrcColors
from core.util import truncate, threaded
from re import IGNORECASE
from html import unescape
from bs4 import BeautifulSoup
import requests


class Chan(Module):

    api_url = "https://a.4cdn.org/{board}/thread/{thread}.json"
    template_thread_info = "{green}{thread} - {blue}{name}{yellow}{trip}{reset} | {red}r:{responses} i:{images}{reset} "

    @on_regex(r'https?:\/\/boards.4chan.org/(\w+)/thread/(\d+)', flags=IGNORECASE)
    @threaded
    def match_bots(self, bot, channel, user, message, match):
        url = Chan.api_url.format(board=match.group(1), thread=match.group(2))
        data = requests.get(url).json()['posts']

        response = Chan.template_thread_info.format(
            thread=match.group(2),
            name=unescape(data[0].get('name', 'Anonymous')),
            trip=data[0].get('trip', ''),
            responses=len(data),
            images=data[0].get('images', 0),
            **IrcColors
        )

        if 'sub' in data[0]:
            response += " | " + truncate(unescape(data[0]['sub']))
        if 'com' in data[0]:
            comment = BeautifulSoup(data[0]['com'], 'html.parser').text
            comment = ' '.join(line if line[0] != '>'
                               else "{green}{line}{reset}".format(line=line, **IrcColors)
                               for line in comment.split('\n') if len(line) > 0)
            response += " | " + truncate(comment, 40)

        bot.message(channel, response)



