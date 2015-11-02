from core import Module, on_command
from bs4 import BeautifulSoup
from core.util import truncate, threaded
import requests


class Eval(Module):

    api_url = "https://eval.in/"
    api_data = {'utf8': 'λ', 'execute': 'on', 'private': 'on', 'input': ''}

    @threaded
    def eval_code(self, bot, channel, user, code, language):
        data = dict(self.api_data)
        data['code'] = code
        data['lang'] = language

        raw = requests.post(self.api_url, data=data)
        soup = BeautifulSoup(raw.text, 'html.parser')

        response = soup.findAll('pre')[-1].text
        response = response.rstrip().replace('\001', '')
        if '\n' in response or '\r' in response:
            bot.message(channel, "{user}: {paste}".format(user=user, paste=raw.url))
        elif len(response) > 300:
            bot.message(channel, truncate(response, 300))
            bot.message(channel, "{user}: {paste}".format(user=user, paste=raw.url))
        else:
            bot.message(channel, response)

    @on_command('py')
    def eval_python3(self, *argv):
        self.eval_code(*argv, language='python/cpython-3.4.1')

    @on_command('py2')
    def eval_python2(self, *argv):
        self.eval_code(*argv, language='python/cpython-2.7.8')

    @on_command('php')
    def eval_php(self, bot, channel, user, code):
        code = "<?php {}".format(code)
        self.eval_code(bot, channel, user, code, language='php/php-5.5.14')
    
    @on_command('js')
    def eval_js(self, *argv):
        self.eval_code(*argv, language='javascript/node-0.10.29')

    @on_command('hs')
    def eval_haskell(self, *argv):
        self.eval_code(*argv, language='haskell/hugs98-sep-2006')



