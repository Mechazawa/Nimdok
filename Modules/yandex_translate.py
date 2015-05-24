"""
Yandex.Translate Nimdok module

API documentation:
https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/
"""


from apikeys import yandex_translate
import requests
from BotKit import command


ENDPOINT = 'https://translate.yandex.net/api/v1.5/tr.json/{verb}'
USAGE = 'Usage, :ytr {in-out|out} text'


@command('ytr')
def parse(bot, channel, user, arg):
    try:
        lang, text = arg.split(' ', 1)
    except ValueError:
        bot.msg(channel, USAGE)
        return

    jo = translate(lang, text)
    code = jo['code']
    if code == 501:
        langs_list = '\n'.join(get_langs()['dirs'])
        # XXX: Nimdok needs SSL with SNI to use nnmm.nl with verification.
        url = requests.post('https://nnmm.nl/', langs_list, verify=False).text
        bot.msg(channel, '{}: Invalid language; full list: {} ({})'.format(
            user,
            url,
            USAGE,
        ))
        return
    elif code != 200:
        errfmt = 'Yandex.Translate responded with error code {}'
        raise ValueError(errfmt.format(code))

    strings = [s.encode('utf-8', 'ignore') for s in jo['text']]
    bot.msg(channel, '{user}: {text}'.format(
        user=user,
        text=' '.join(strings),
    ))


def call_yandex_api(verb, parameters=None):
    if parameters is None:
        parameters = {}
    url = ENDPOINT.format(verb=verb)
    parameters['key'] = yandex_translate
    resp = requests.get(url, params=parameters)
    return resp.json()


def get_langs():
    return call_yandex_api('getLangs')


def translate(lang, text):
    return call_yandex_api('translate', {
        'text': text,
        'lang': lang,
        'format': 'text',
    })
