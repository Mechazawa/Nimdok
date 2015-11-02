from core import on_regex, Module
from core.util import threaded
from core.color import IrcColors
from models import ApiKeyModel
import requests


class Youtube(Module):
    _base_url = "https://www.googleapis.com/youtube/v3/videos?id={video}&key={key}&part=snippet,statistics"
    _template = "{title} | {channel} {green}↑{likes:,} {red}↓{dislikes:,}{reset} | {views:,} views"

    @on_regex(r'https?://(?:www\.)?(?:youtu\.be|youtube.\w{2,}.+)(?:\W|^)([A-Za-z0-9\-_]{11})(?:\W|$)')
    def on_youtube(self, bot, channel, user, message, matches):
        video = matches.group(1)
        info = self.get_info(video)

        info.update(IrcColors)
        bot.message(channel, self._template.format(**info))

    def get_info(self, video):
        url = self._base_url.format(video=video, key=self._api_key)
        json = requests.get(url).json()
        data = json['items'][0]
        data_stats = data['statistics']
        data_info = data['snippet']

        return {
            'channel': data_info['channelTitle'],
            'title': data_info['title'],
            'likes': int(data_stats['likeCount']),
            'dislikes': int(data_stats['dislikeCount']),
            'views': int(data_stats['viewCount']),
        }

    @property
    def _api_key(self):
        return ApiKeyModel.get('youtube').key

