from core import Module, on_command, util
import requests


class VirtualCurrencies(Module):
    """
    Allows you to get the current value of virtual currencies
    """

    template = "{currency} · Buy: {buy}$ · Sell: {sell}$ · Last: {last}$ · High: {high}$ · Low: {low}$ · bter.com"
    url = "http://data.bter.com/api/1/ticker/{}_usd"

    def _build_message(self, currency):
        data = requests.get(self.url.format(currency)).json()
        return self.template.format(currency=currency.upper(), **data)

    @on_command('btc')
    @util.threaded
    def btc(self, bot, channel, user, args):
        bot.message(channel, self._build_message('btc'))

    @on_command("doge")
    @util.threaded
    def doge(self, bot, channel, user, args):
        bot.message(channel, self._build_message('doge'))

    @on_command("ltc")
    @util.threaded
    def ltc(self, bot, channel, user, args):
        bot.message(channel, self._build_message('ltc'))
