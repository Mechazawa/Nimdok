import time
from core import Module, on_command
from models import AdminModel, db_session
from core import util
from tornado.ioloop import IOLoop


def requires_admin_privileges(f):
    def decorated(self, bot, channel, user, *args, **kwargs):
        admin = Admin.is_admin(bot, user)
        if admin:
            return f(self, bot, channel, user, *args, **kwargs)
        else:
            bot.message(channel, Admin.template_denied.format(user=user))

    return util.threaded(decorated)


class Admin(Module):
    """
    This module manages the admin privileges
    """

    template_denied = "Sorry, {user}, I can't let you do that"
    template_add_help = "{user}, usage: :adminadd [user]"

    @on_command('adminadd')
    @requires_admin_privileges
    def match_bots(self, bot, channel, user, args):
        args = args.split()
        if len(args) != 1:
            bot.message(channel, Admin.template_add_help.format(user=user))
        else:
            username = args[0]

            if Admin.is_admin(bot, username):
                bot.message(channel, "{user} is already an admin".format(user=username))
            else:
                AdminModel.insert(username=username.upper())
                bot.message(channel, "{user} has been added to the admin list".format(user=username))

    @on_command('beep')
    @requires_admin_privileges
    def test(self, bot, channel, user, args):
        bot.message(channel, "Yay")

    @staticmethod
    def is_admin(bot, nickname):
        print("testing admin")
        # Is the user listed as an admin?
        admin = AdminModel.query \
                    .filter_by(username=nickname.upper()) \
                    .count() > 0

        # Is the user authenticated into the services?
        if admin:
            info = bot.whois(nickname)
            while not info.done():
                time.sleep(0.01)

            info = info.result()
            admin = info['identified']

        return admin
