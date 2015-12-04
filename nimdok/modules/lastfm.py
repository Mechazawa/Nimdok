from core import Module, on_command, on_regex
from models import LastfmModel, ApiKeyModel
from re import compile, IGNORECASE
import requests


class Lastfm(Module):
    api_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&format=json&limit=1'
    collage_url = 'http://nsfcd.com/lastfm/collage.php?user=%s&type=7day&size=%s&caption=true'
    collage_size_regex = r':np ((?:[1-9]|10)x(?:[1-9]|10))$'

    @on_command('np register')
    def command_register(self, bot, channel, user, args):
        if len(args.split()) > 1:
            bot.message(channel, "{user}: please only enter one username".format(user=user))
        elif len(args.strip()) is 0:
            bot.message(channel, 'usage: :np register [lastfm username]')
        else:
            LastfmModel.set(user, args)

    @on_command('np')
    def command_np(self, bot, channel, user, args):
        if len(args.strip()) > 0:
            return

        lastfm_nick = LastfmModel.get(user)
        if lastfm_nick is None:
            bot.message(channel, "{user}: I don't know you. Use :np register [lastfm username]")
            return

        api_key = ApiKeyModel.get('lastfm')
        url = Lastfm.api_url.format(api_key=api_key, user=lastfm_nick)
        data = requests.get(url).json()
        track = data['recenttracks']['track']

        if isinstance(track, list):
            track = track[0]


    @on_regex(collage_size_regex, flags=IGNORECASE)
    def regex_collage(self, bot, channel, user, message, match):
        pass

