import time
from core import Module, on_command
from models import AdminModel, ModuleModel, db
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
    template_module_not_found = "{user}: {module} could not be found"
    template_module_enabled = "{user}: enabled {module}"
    template_module_already_enabled = "{user}: {module} was already enabled"
    template_module_disabled = "{user}: disabled {module}"
    template_module_already_disabled = "{user}: {module} was already disabled"

    @on_command('admin add')
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

    @on_command('admin remove')
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

    @on_command('module enable')
    @requires_admin
    def command_mod_enable(self, bot, channel, user, args):
        module = args.split(' ', 1)[0]
        if bot.find_module(module) is None:
            message = self.template_module_not_found.format(user=user, module=module)
        elif ModuleModel.enable(module):
            message = self.template_module_enabled.format(user=user, module=module)
            bot.init_modules()
        else:
            message = self.template_module_already_enabled.format(user=user, module=module)

        bot.message(channel, message)

    @on_command('module disable')
    @requires_admin
    def command_mod_disable(self, bot, channel, user, args):
        module = args.split(' ', 1)[0]
        if bot.find_module(module) is None:
            message = self.template_module_not_found.format(user=user, module=module)
        elif ModuleModel.disable(module):
            message = self.template_module_disabled.format(user=user, module=module)
            bot.init_modules()
        else:
            message = self.template_module_already_disabled.format(user=user, module=module)

        bot.message(channel, message)

    @on_command('module reload')
    def command_mod_reload(self, bot, channel, user, args):
        bot.init_modules()
        bot.message(channel, 'Reloaded modules')

    @on_command('module list')
    def command_mod_list(self, bot, channel, user, args):
        all = list(map(lambda x: x.__name__, bot.list_modules()))

        enabled = ModuleModel.list_enabled()
        enabled = [x for x in all if x.upper() in enabled]  # Fix uppercase
        disabled = [x for x in all if x not in enabled]

        bot.message(channel, "Enabled: {}".format(', '.join(enabled)))
        bot.message(channel, "Disabled: {}".format(', '.join(disabled)))
