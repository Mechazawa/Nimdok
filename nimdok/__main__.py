from core import nimdok

bot = nimdok.Nimdok('Nimdok')
bot.connect('irc.rizon.net', 6697, tls=True, tls_verify=False)
bot.handle_forever()