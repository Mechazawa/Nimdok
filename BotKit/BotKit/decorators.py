_commands = []
_callbacks = []


def command(name, restricted=False):
    global _commands
    def decorator(f):
        _commands.append({
            "command": name.lower(),
            "method": f,
            "restricted": restricted
        })
    return decorator

def handles(type, raw=False):
    global _callbacks
    def decorator(f):
        _callbacks.append({
            "type": type,
            "method": f,
            "raw": raw
        })
    return decorator

def getcommand(name):
    global _commands
    return [c for c in _commands if c['command'] == name.lower()]

def getcallback(name, raw=False):
    global _callbacks
    return [c['method'] for c in _callbacks if c['type'] == name.lower() and c['raw'] == raw]
