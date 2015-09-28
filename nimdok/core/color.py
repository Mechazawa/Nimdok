from itertools import permutations

"""
usage:
  "{green}beep {yellow_blue}boop".format(**IrcColor)
"""

IrcColors = {
    'LBlue': 12, 'LCyan': 11,
    'LBrown': 5, 'LMagenta': 13,
    'LGray': 15, 'Yellow': 8,
    'White': 0, 'Blue': 2,
    'Gray': 14, 'Green': 3,
    'Red': 4, 'Black': 1,
    'Cyan': 10, 'LGreen': 9,
    'Orange': 7, 'Magenta': 6
}


def _init():
    if len(IrcColors) > 16:
        return

    colormap_new = dict(map(
        lambda x: (x, "\x03{0:02}\x02\x02".format(IrcColors[x])),
        IrcColors
    ))

    colormap_new.update(dict(map(
        lambda x: (
            "{0}_{1}".format(*x),
            "\x03{0:02},{1:02}".format(IrcColors[x[0]], IrcColors[x[1]])
        ), list(permutations(IrcColors, 2)) + list(map(lambda c: (c, c), IrcColors))
    )))

    colormap_new_lowercase = {}
    for name, value in colormap_new.items():
        colormap_new_lowercase[name.lower()] = value

    IrcColors.update(colormap_new)
    IrcColors.update(colormap_new_lowercase)
    IrcColors['reset'] = '\x03'

_init()

