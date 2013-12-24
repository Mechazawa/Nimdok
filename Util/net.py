import HTMLParser

def getdomain(s, nosub=False):
    domain = s.split('/')[2].split('?')[0]
    return domain.split('.', domain.count(".")-1)[-1] if nosub else domain

def unescape(s):
    return HTMLParser.HTMLParser().unescape(s)