import os

imported = []
for module in os.listdir('modules'):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    else:
        imported.append(module[:-3])
        exec("import modules.%s" % module[:-3])