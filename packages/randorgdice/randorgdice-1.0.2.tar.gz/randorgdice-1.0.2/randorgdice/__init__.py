import urllib, threading, re
from urllib import parse, request

__version__ = "1.0.0"
__url__ = "https://pypi.org/project/randorgdice/"
_LOCK = threading.Lock()

def _fetch_rorg(service="integers", user_agent="randorgdice", **args):
    url = "http://random.org/%s/?%s"
    parameters = dict(format='plain', num=1, col=1, min=1, max=10, base=10)
    parameters.update(args)
    url = url % (service, urllib.parse.urlencode(parameters))
    headers = {
        'User-Agent': '%s/RandomDotOrgPyV%s + %s' % (
            user_agent, __version__, __url__)
    }
    request = urllib.request.Request(url, headers=headers)
    with _LOCK:
        results = urllib.request.urlopen(request).read()
    return results.splitlines()

def fetch_integers(num=1,min=1,max=20):
    fetch_list = _fetch_rorg(service="integers", user_agent="randorgdice", format="plain", num=num, col=1, min=min, max=max)
    string = "".join(str(fetch_list))
    return [int(n) for n in re.findall(r'-{,1}\d{1,}', string)]