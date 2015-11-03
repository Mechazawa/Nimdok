from core import nimdok
from argparse import ArgumentParser
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import declarative_base, ModuleModel, db

parser = ArgumentParser(description='Nimdok; the modular irc bot')

parser_server = parser.add_argument_group('server')
parser_server.add_argument('-s', '--server', metavar='SRV', help='the IRC server', default='irc.rizon.net')
parser_server.add_argument('-p', '--port', metavar='NUM', type=int, help='the server port', default=6667)
parser_server.add_argument('-c', '--channels', metavar='C', help='comma separated channels to connect to',
                           default='#bots,#spam')
parser_server.add_argument('--ssl', action='store_true', help='connect using SSL')
parser_server.add_argument('--ssl-no-verify', action='store_true', help='accept any ssl cert')

parser_ident = parser.add_argument_group('identity')
parser_ident.add_argument('-n', '--nickname', help='nickname', metavar='NICK', default='Nimdok')
parser_ident.add_argument('-u', '--username', help='username', metavar='USER', default='bot')
parser_ident.add_argument('-r', '--realname', help='realname', metavar='NAME', default='bot')
parser_ident.add_argument('-P', '--password', help='password', metavar='PASS', default='')

#parser.add_argument('-C', '--config', metavar='CFG', help='config to read', type=FileType('r'))
#parser.add_argument('--create-config', metavar='FILE', help='dump current arguments to a config file',
#                    type=FileType('w'))
parser.add_argument('--init-db', help='initialize database', action='store_true')
parser.add_argument('-d', '--database', metavar='URI', help='database uri (default: sqlite:///nimdok.db)',
                    default='sqlite:///nimdok.db')
parser.add_argument('--debug', action='store_true')


args = parser.parse_args()

print('Opening database connection')
db.engine = create_engine(args.database)
db.session = scoped_session(sessionmaker(bind=db.engine))
declarative_base.query = db.session.query_property()


if args.init_db is True:
    print('Creating tables')
    declarative_base.metadata.create_all(bind=db.engine)
    db.session.commit()
    print('Created tables')
    for module in nimdok.Nimdok.list_modules():
        ModuleModel.enable(module)
    print('Enabled all modules')

bot = nimdok.Nimdok(args.nickname, username=args.username, realname=args.realname)
bot.connect(
    args.server, args.port,
    channels=args.channels.split(','),
    tls=args.ssl, tls_verify=not args.ssl_no_verify
)
bot.logger.setLevel(10 if args.debug is True
                    else 20)
bot.handle_forever()
