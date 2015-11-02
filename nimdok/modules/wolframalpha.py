from core import Module, on_command
from core.util import threaded
from models import ApiKeyModel
from xml.etree import cElementTree
import requests


class WolframAlpha(Module):
    _base_url = 'http://api.wolframalpha.com/v2/query'
    _base_params = {
        'units': 'metric',
        'location': 'Amsterdam',
        'reinterpret': 'true',
        'format': 'plaintext',
        'excludepodid': 'Input',
    }

    @on_command('wa')
    def command_wolfram(self, bot, channel, user, message):
        tree = self._api_request(message)

        if tree.get('error') != 'false':
            bot.message(channel, "WolframAlpha returned an error")
        elif int(tree.get('numpods')) > 0:
            result = tree.find('pod')\
                         .find('subpod')\
                         .find('plaintext').text

            bot.message(channel, "{user}: {result}".format(user=user, result=result))
        else:
            bot.message(channel, "{user}: Couldn't find what you were looking for".format(user=user))

    @property
    def _api_key(self):
        return ApiKeyModel.get('wolframalpha').key

    def _api_request(self, query):
        params = {}
        params.update(self._base_params)
        params['appid'] = self._api_key
        params['input'] = query

        response = requests.get(self._base_url, params=params).text
        print(response)
        return cElementTree.fromstring(response)
