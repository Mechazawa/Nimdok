from core import Module, on_command
from .admin import requires_admin
from models import ApiKeyModel
import requests


class ApiKeys(Module):

    @on_command('apikey set')
    @requires_admin
    def command_set(self, bot, channel, user, args):
        if channel[0] == '#':
            bot.message(user, "{user}: This command can only be ran by pm-ing the bot".format(user=user))
            return

        args = args.split(maxsplit=1)
        if len(args) != 2:
            bot.message(user, 'Usage: :setkey [api] [key]')
            return

        ApiKeyModel.set(*args)
        bot.message(user, "Set key for {api}".format(api=args[0]))

    @on_command('apikey list')
    @requires_admin
    def command_list(self, bot, channel, user, args):
        if channel[0] == '#':
            bot.message(user, "{user}: This command can only be ran by pm-ing the bot".format(user=user))
        else:
            keys = ApiKeyModel.list()
            data = '\n'.join("{}: {}".format(*k) for k in keys.items())
            url = requests.post('https://nnmm.nl', data=data).text
            bot.message(user, url)
