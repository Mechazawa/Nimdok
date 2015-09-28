from core import Module, on_command, IrcColors
from core.util import threaded
import json
import requests


class Dns(Module):

    template_domain_usage = "Usage: :domain example com net org"
    template_domain_output = "{domain}"
    domain_api = "https://instantdomainsearch.com/all/{domain}?tlds={tlds}&limit=1"

    @on_command("domain")
    @threaded
    def command_domain(self, bot, channel, user, args):
        args = args.split()
        if len(args) < 2:
            bot.message(channel, Dns.template_domain_usage)
            return

        domain = args[0]
        del args[0]
        result = {}

        url = Dns.domain_api.format(domain=domain, tlds=','.join(args))
        raw = requests.get(url).text.strip()
        for line in raw.split('\n'):
            js = json.loads(line)
            if 'isRegistered' in js:
                result[js['tld']] = js['isRegistered']

        output = Dns.template_domain_output.format(domain=domain)
        taken = list(filter(lambda x: result[x] is True, result))
        avail = list(filter(lambda x: result[x] is False, result))

        if len(avail) > 0:
            output += " {green}A: {tld}".format(tld=', '.join(avail), **IrcColors)
        if len(taken) > 0:
            output += " {red}T: {tld}".format(tld=', '.join(taken), **IrcColors)

        bot.message(channel, output)