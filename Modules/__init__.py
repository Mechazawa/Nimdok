# -*- coding: utf-8 -*-

import os

imported = []
for module in os.listdir('Modules'):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    else:
        imported.append(module[:-3])
        exec("import Modules.%s" % module[:-3])
