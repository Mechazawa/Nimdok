import os

try: loadedmodules
except: loadedmodules = []

for module in os.listdir('modules'):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        if module[:-3] in loadedmodules:
            exec("reload(%s)"%module[:-3])
        else:
            exec("import modules.%s" % module[:-3])
            loadedmodules.append(module[:-3])


print "loaded %i modules" % len(loadedmodules)
print ', '.join(loadedmodules)