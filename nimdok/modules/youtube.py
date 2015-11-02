from core import on_regex, Module
from core.color import IrcColors
from models import ApiKeyModel
import requests


class Youtube(Module):
    _base_url = "https://www.googleapis.com/youtube/v3/videos"
    _template = "{title} | {channel} {green}↑{likes:,} {red}↓{dislikes:,}{reset} | {views:,} views"

    @on_regex(r'https?://(?:www\.)?(?:youtu\.be|youtube.\w{2,}.+)(?:\W|^)([A-Za-z0-9\-_]{11})(?:\W|$)')
    def on_youtube(self, bot, channel, user, message, matches):
        video = matches.group(1)
        info = self.get_info(video)

        info.update(IrcColors)
        bot.message(channel, self._template.format(**info))

    def get_info(self, video):
        params = {
            'key': self._api_key,
            'id': video,
            'part': 'snippet,statistics',
        }

        response = requests.get(self._base_url, params=params).json()
        print(response)
        response = response['items' if 'items' in response else 'videos']

        stats = response['statistics']
        info = response['snippet']

        return {
            'channel': info['channelTitle'],
            'title': info['title'],
            'likes': int(stats['likeCount']),
            'dislikes': int(stats['dislikeCount']),
            'views': int(stats['viewCount']),
        }

    @property
    def _api_key(self):
        return ApiKeyModel.get('youtube').key

