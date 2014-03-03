from BotKit import ignore, command
import urllib2

@command('ignore', True)
def parse(bot, channel, user, args):
    usr = args.split()[0]
    if ignore().isignored(usr):
        bot.msg(channel, "%s: %s is already being ignored" % (user, usr))
    else:
        ignore().add(usr)
        bot.msg(channel, "%s: I never liked %s anyway" % (user, usr))

@command('ignored')
def parse(bot, channel, user, args):
    paste = urllib2.urlopen("https://nnmm.nl/", ', '.join(ignore().getignores())).read()
    bot.msg(channel, "%s: %s" % (user, paste))

@command('acknowledge', True)
def parse(bot, channel, user, args):
    usr = args.split()[0]
    if usr.lower() == user.lower():
        bot.msg(channel, 'shit, what are you doing son')

    if ignore().isignored(usr):
        ignore().remove(usr)
        bot.msg(channel, "%s: I'm now acknowledging %s's existence" % (user, usr))
    else:
        bot.msg(channel, "%s: I'm not ignoring %s" % (user, usr))
