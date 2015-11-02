from core import Module, on_command
from core.util import threaded
from models import ApiKeyModel
import requests


class Translate(Module):

    _template_usage = "{user}: Usage, :tr {in-out|out} text"
    _template_invalid = "{user}: Invalid language, full list {url}"
    _endpoint = "https://translate.yandex.net/api/v1.5/tr.json/{command}"

    _languages = None  # Language cache

    def _call_api(self, command, parameters=None):
        if not parameters:
            parameters = {}

        url = self._endpoint.format(command=command)
        parameters['key'] = self._api_key

        response = requests.get(url, params=parameters)
        return response.json()

    @property
    def _api_key(self):
        return ApiKeyModel.get('yandex_translate').key

    @property
    def languages(self):
        if self._languages is None:
            self._languages = self._call_api('getLangs')['dirs']

        return self._languages

    def translate(self, text, target_language='en'):
        data = {
            'text': text,
            'lang': target_language,
            'format': 'text',
        }

        return self._call_api('translate', data)

    @on_command('tr')
    @threaded
    def command_translate(self, bot, channel, user, params):
        try:
            lang, text = params.split(' ', 1)
        except:
            bot.message(channel, self._template_usage.format(user=user))
            return

        json = self.translate(text, lang)
        response_code = json['code']
        if response_code == 501:
            languages = ', '.join(self.languages)
            url = requests.post('https://nnmm.nl', data=languages).text

            bot.message(channel, self._template_invalid.format(user=user, url=url))

        elif response_code == 200:
            text = ' '.join(json['text'])
            if len(text) > 200:
                text = requests.post('https://nnmm.nl', data=text).text

            bot.message(channel, "{user}: {text}".format(user=user, text=text))

        else:
            raise Exception("Yandex api responded with unknown response code {}".format(response_code))

