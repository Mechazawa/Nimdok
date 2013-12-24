import re

def sizefmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def intcomma(value):
    try:
        if isinstance(value, str):
            float(value.replace(',', ''))
        else:
            float(value)
    except (TypeError, ValueError):
        return value
    orig = str(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new)

powers = [10 ** x for x in (6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
human_powers = ['million', 'billion', 'trillion', 'quadrillion',
                'quintillion', 'sextillion', 'septillion',
                'octillion', 'nonillion', 'decillion', 'googol']
def intword(value, format='%.1f'):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    if value < powers[0]:
        return str(value)
    for ordinal, power in enumerate(powers[1:], 1):
        if value < power:
            chopped = value / float(powers[ordinal - 1])
            return (' '.join([format, human_powers[ordinal - 1]])) % chopped
    return str(value)