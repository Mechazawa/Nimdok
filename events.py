try: events
except: events = {}

def setEvent(hook, name, function):
    try: events[hook]
    except: events[hook] = {}
    events[hook][name] = function

def getEvents(hook):
    try: return [events[hook][e] for e in events[hook]]
    except: return []