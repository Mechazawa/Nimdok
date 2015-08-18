import os

imported = []
for module in os.listdir('nimdok/modules'):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    else:
        imported.append(module[:-3])
        exec("from modules import %s" % module[:-3])

