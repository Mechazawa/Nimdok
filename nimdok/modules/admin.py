import time
from core import Module, on_command
from models import AdminModel, db
from core import util


def requires_admin(f):
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
    template_add_help = "{user}, usage: :addadmin [user]"
    template_add_exists = "{user} is already an adrmmin"
    template_add_success = "{user} has been added to the admin list"
    template_rm_help = "{user}, usage: :rmadmin [user]"
    template_rm_not_found = "{user} is not an admin"
    template_rm_success = "{user} has been removed from the admin list"

    @on_command('addadmin')
    @requires_admin
    def command_admin_add(self, bot, channel, user, args):
        args = args.split()
        if len(args) != 1:
            bot.message(channel, Admin.template_add_help.format(user=user))
        else:
            username = args[0]

            if AdminModel.is_admin(username):
                bot.message(channel, Admin.template_add_exists.format(user=username))
            else:
                admin = AdminModel(username.upper())
                db.session.add(admin)
                db.session.commit()
                bot.message(channel, Admin.template_add_success.format(user=username))

    @on_command('rmadmin')
    @requires_admin
    def command_admin_rm(self, bot, channel, user, args):
        args = args.split()
        if len(args) != 1:
            bot.message(channel, Admin.template_rm_help.format(user=user))
        else:
            username = args[0]
            if not AdminModel.is_admin(username):
                bot.message(channel, Admin.template_rm_not_found.format(user=username))
            else:
                AdminModel.query.filter_by(username=username.upper()).remove()
                db.session.commit()
                bot.message(channel, Admin.template_rm_success.format(user=username))

    @staticmethod
    def is_admin(bot, nickname):
        # Is the user listed as an admin?
        admin = AdminModel.is_admin(nickname)

        # Is the user authenticated into the services?
        if admin:
            info = bot.whois(nickname)
            while not info.done():
                time.sleep(0.01)

            info = info.result()
            admin = info is not None and info['identified']

        return admin
