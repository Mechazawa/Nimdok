_commands = []
_callbacks = []


def command(name, restricted=False):
    global _commands
    def decorator(f):
        _commands.append({
            "command": name,
            "method": f,
            "restricted": restricted
        })
    return decorator

def handles(type, cctp=False):
    global _callbacks
    def decorator(f):
        _callbacks.append({
            "type": type,
            "cctp": cctp,
            "method": f
        })
    pass