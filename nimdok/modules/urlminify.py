import requests
from core import Module, on_regex, on_command, util


class UrlMinify(Module):
    def __init__(self, bot):
        super().__init__(bot)
        self.last_url = {}

    @on_regex(r'(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])')
    def match_url(self, bot, channel, user, message, matches):
        self.last_url[channel] = matches.group(1)

    @on_command('minify')
    @util.threaded
    def minify_url(self, bot, channel, user, args):
        url = self.last_url.get(channel, 'https://rms.sexy')
        url = requests.post('https://nnmm.nl', data=url)
        bot.message(channel, "{}: {}".format(user, url))
