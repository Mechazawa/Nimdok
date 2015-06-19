from BotKit import command
from BotKit.BotKit.util.stylize import SetColor, Color, Truncate
from dns import resolver
from collections import namedtuple
import re

VALID_RTYPES = {
    'A': lambda r: r.address,
    'AAAA': lambda r: r.address,
    'CNAME': lambda r: r.target,
    'MX': lambda r: '{} priority {}'.format(r.exchange, r.preference),
    'NS': lambda r: r.target,
    'SRV': lambda r: '{} port {} priority {} weight {}'.format(r.target,
                                                               r.port,
                                                               r.priority,
                                                               r.weight),
    'TXT': lambda r: Truncate(re.sub(r'\r|\n', '', r.strings[0])),
}
Arguments = namedtuple('Arguments', ('index', 'rtype', 'domain'))

@command('dns')
def parse(bot, channel, user, args):
    params = parse_args(args)

    if params is None:
        bot.msg(channel, 'Usage -- :dns [{}] domain [-n]'.format(
            '|'.join(sorted(VALID_RTYPES)),
        ))
        return

    index, rtype, domain = params
    list_index = index - 1

    resolver_ = resolver.get_default_resolver()
    resolver_.timeout = 5.0

    query_text = SetColor('{} in {}'.format(domain, rtype), Color.Orange)
    L = [query_text]
    try:
        res = resolver_.query(domain, rtype)
        item = res[min(len(res), list_index)]
    except (resolver.NXDOMAIN, resolver.NoAnswer):
        L.append(SetColor('does not exist.', Color.Red))
    else:
        record_text = VALID_RTYPES[rtype](item)
        record_text = SetColor(record_text, Color.Green)
        L.append(record_text)
        if len(res) > 1:
            L.append(SetColor('({}/{})'.format(index, len(res)),
                              Color.LBlue))

    message = ' '.join(L)
    bot.msg(channel, message)


def parse_args(args):
    L = args.split(' ')
    if len(L) == 1:
        index = '1'
        rtype = 'A'
        domain = L[0]
    elif len(L) == 2:
        if L[1].startswith('-'):
            index = L[1][1:]
            rtype = 'A'
            domain = L[0]
        else:
            index = '1'
            rtype = L[0]
            domain = L[1]
    elif len(L) == 3:
        if L[2].startswith('-'):
            index = L[2][1:]
        else:
            return None
        rtype = L[0]
        domain = L[1]
    else:
        return None
    rtype = rtype.upper()
    domain = domain.lower()
    if not index.isdigit() or int(index) < 1:
        return None
    if rtype not in VALID_RTYPES:
        return None
    if not domain:
        return None
    return Arguments(int(index), rtype, domain)
