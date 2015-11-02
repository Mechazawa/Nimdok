from core import Module, on_command
from core.util import threaded
import requests


class UrbanDictionary(Module):
    _template_undefined = "{user}: That word is not defined"
    _template_response = "{word} - {definition:.100}"
    _base_url = "http://api.urbandictionary.com/v0/{endpoint}"

    @on_command('ud')
    @threaded
    def command_urban(self, bot, channel, user, message):
        message = message.strip()
        params = {}
        if message == '':
            url = self._base_url.format(endpoint='random')
        else:
            url = self._base_url.format(endpoint='define')
            params['term'] = message

        response = requests.get(url, params=params).json()
        if len(response['list']) is 0:
            bot.message(channel, self._template_undefined.format(user=user))
        else:
            data = response['list'][0]
            bot.message(channel, self._template_response.format(**data))
