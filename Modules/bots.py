# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import stylize, handles


@handles('msg')
def parse(bot, channel, user, msg):
    if msg.lower()[:6].rstrip() == ".bots":
        bot.msg(channel, 
                "Reporting in! " + 
                stylize.SetColor("[Python] ", stylize.Color.Blue) + 
                stylize.SetColor("See " + stylize.Bold("https://github.com/Mechazawa/Nimdok"), stylize.Color.Cyan)
        )
