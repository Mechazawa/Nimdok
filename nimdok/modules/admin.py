from core import Module, on_command
from models import AdminModel, db_session
from core import util


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
    Basic module that fulfills the requirement that
    it should respond to .bots
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
            db_session.add(AdminModel(args[0]))
            db_session.commit()
            bot.message(channel, "beep " + args[0])

    @on_command('beep')
    @requires_admin_privileges
    def test(self, bot, channel, user, args):
        bot.message(channel, "Yay")

    @staticmethod
    def is_admin(bot, nickname):
        # Is the user listed as an admin?
        admin = db_session.query(AdminModel)\
                     .filter_by(username=nickname.upper())\
                     .one_or_none() is not None

        # Is the user authenticated into the services?
        if admin:
            info = yield bot.whois()
            admin = info['identified']

        return admin
