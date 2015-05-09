# -*- coding: utf-8 -*-

import requests
import re
from urlparse import urlparse, parse_qs
from BotKit import handles, stylize, humanize
from apikeys import google

YT_REGEX = re.compile(r'(?:\W|^)([A-Za-z0-9\-_]{11})(?:\W|$)')
API_URL = ('https://www.googleapis.com/youtube/v3/videos'
          '?part=snippet,statistics&id={vid}&key={apikey}')

@handles('msg')
def parse(bot, channel, user, msg):
    for m in msg.split(' '):
        parts = urlparse(m)

        if parts.scheme not in ['http', 'https']:
            continue

        if 'youtube.' in parts.netloc:
            L = parse_qs(parts.query).get('v', '')
            s = L[0] if L else ''
        elif 'youtu.be' in parts.netloc:
            s = parts.path
        else:
            continue

        matches = YT_REGEX.search(s)
        if matches is None:
            bot.logger.info('No youtube id found.')
            continue
        vid = matches.group(1)
        bot.logger.info('Matched youtube id: {}'.format(vid))

        req_url = API_URL.format(
            apikey=google,
            vid=vid,
        )

        resp = requests.get(req_url)
        jo = resp.json()
        if jo['pageInfo']['totalResults'] < 1:
            bot.logger.info('Bad youtube id: {}'.format(vid))
            continue
        entry = jo['items'][0]
        stats, snippet = entry['statistics'], entry['snippet']

        views = int(stats['viewCount'])
        dislikes = int(stats['dislikeCount'])
        likes = int(stats['likeCount'])
        yt_channel = snippet['channelTitle']
        title = snippet['title']

        fmt = u'{title} | {channel} {likes} {dislikes} | {views} views'
        message = fmt.format(
            title=stylize.Bold(stylize.Trunicate(title)),
            channel=yt_channel,
            likes=format_likes(likes),
            dislikes=format_dislikes(dislikes),
            views=format_views(views),
        ).encode('utf-8', 'ignore')
        bot.msg(channel, message)

def format_views(views):
    fn = humanize.intcomma if views < 1000000 else humanize.intword
    return fn(views)

def format_likes(likes):
    return stylize.SetColor(u'↑' + humanize.intcomma(likes),
                            stylize.Color.Green)

def format_dislikes(dislikes):
    return stylize.SetColor(u'↓' + humanize.intcomma(dislikes),
                            stylize.Color.Red)
