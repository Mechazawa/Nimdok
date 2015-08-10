from threading import Thread


# http://stackoverflow.com/a/26151604
def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def threaded(f):
    def decorated(*args, **kwargs):
        Thread(target=f, args=args, kwargs=kwargs).start()
    return decorated
