from bs4 import BeautifulSoup
from core import Module, on_regex, on_command, util, IrcColors
from .admin import requires_admin
from models import IgnoredDomainModel
from urllib.parse import urlsplit
from humanize import naturalsize
import requests
import re


class Url(Module):

    template_ignore_help = "{user}, usage: :ignoredomain [domain]"
    template_acknowledge_help = "{user}, usage: :acknowledgedomain [domain]"
    template_acknowledge = "Removed {domain} from the blacklist"
    template_ignore = "Added {domain} to the blacklist"
    template_domain_invalid = "{user}, '{domain}' is not a valid domain name"
    regex_domain = re.compile(r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|'
                              r'([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))'
                              r'\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$')

    def __init__(self, bot):
        super().__init__(bot)
        self.last_url = {}

    @on_regex(r'(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])')
    @util.threaded
    def match_url(self, bot, channel, user, message, matches):
        return #disabled for now

        url = matches.group(1)
        self.last_url[channel] = url

        domain = urlsplit(url).netloc
        if IgnoredDomainModel.is_ignored(domain):
            return

        head = requests.request('HEAD', url)
        mime = head.headers['content-type']

        if 'html' in mime.lower():
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            title = soup.find('title')

            if title is not None:
                title = title.text
            else:
                title = soup.text

            title = title.replace('\r', '').replace('\n', '').replace('\x01', '')
            title = util.truncate(title, 250)
            bot.message(channel, title)
        elif 'text' in mime.lower():
            text = requests.get(url).text
            text = text.replace('\r', '').replace('\n', '').replace('\x01', '')
            text = util.truncate(text, 250)
            bot.message(channel, text)
        else:
            size = int(head.headers.get('content-length', 0))
            bot.message(channel, "{mime} - {size}".format(mime=mime, size=naturalsize(size), **IrcColors))

    @on_command('minify')
    @util.threaded
    def minify_url(self, bot, channel, user, args):
        url = self.last_url.get(channel, 'https://rms.sexy')
        url = requests.post('https://nnmm.nl', data=url).text
        bot.message(channel, "{}: {}".format(user, url))

    @on_command('ignoredomain')
    @requires_admin
    def domain_ignore(self, bot, channel, user, args):
        args = args.split()
        if len(args) is not 1:
            bot.message(channel, self.template_ignore_help.format(user=user))
            return

        domain = args[0]
        if not self.regex_domain.match(domain):
            bot.message(channel, self.template_domain_invalid.format(user=user, domain=domain))
            return

        IgnoredDomainModel.add(domain)
        bot.message(channel, self.template_ignore.format(domain=domain))

    @on_command('acknowledgedomain')
    @requires_admin
    def domain_acknowledge(self, bot, channel, user, args):
        args = args.split()
        if len(args) is not 1:
            bot.message(channel, self.template_acknowledge_help.format(user=user))
            return

        domain = args[0]
        if not self.regex_domain.match(domain):
            bot.message(channel, self.template_domain_invalid.format(user=user, domain=domain))
            return

        IgnoredDomainModel.remove(domain)
        bot.message(channel, self.template_acknowledge.format(domain=domain))

    @on_command('urlblacklist')
    def domain_list_blacklist(self, bot, channel, user, args):
        domains = [x.domain.lower() for x in IgnoredDomainModel.query.all()]
        text = '\n'.join(domains)

        url = requests.post('https://nnmm.nl', data=text).text
        bot.message(channel, "{user}, {url}".format(user=user, url=url))
