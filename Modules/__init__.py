#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try: loadedmodules
except: loadedmodules = []

for module in os.listdir('Modules'):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    if module[:-3] in loadedmodules:
        exec("reload(%s)"%module[:-3])
    else:
        exec("import Modules.%s" % module[:-3])
        loadedmodules.append(module[:-3])


print("loaded %i Modules" % len(loadedmodules))
print(', '.join(loadedmodules))