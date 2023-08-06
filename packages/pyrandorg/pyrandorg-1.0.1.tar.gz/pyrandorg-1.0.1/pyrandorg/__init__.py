import urllib.request
import urllib.parse
import threading
import re
import random

__version__ = "1.0.0"
__url__ = 'https://pypi.org/project/pyrandorg'
_LOCK = threading.Lock()


class Pyrandorg:
    def __init__(self, service="integers"):
        self.__service = service
        self.__user_agent = "pyrandorg"
        self.__seed = 0.1
        self.__latest_results = []

    def fetch_randomdotorg(self, **args):
        url = "http://random.org/%s/?%s"
        parameters = dict(format='plain', num=1, col=1, min=1, max=10, base=10)
        parameters.update(args)
        url = url % (self.__service, urllib.parse.urlencode(parameters))
        headers = {
            'User-Agent': '%s/RandomDotOrgPyV%s + %s' % (
                self.__user_agent, __version__, __url__)
        }
        request = urllib.request.Request(url, headers=headers)
        with _LOCK:
            results = urllib.request.urlopen(request).read()
        if self.__service == "integers":
            return [int(n) for n in re.findall(r'-?\d+', str(results))]
        else:
            return [n for n in re.findall(r'-?\d+\.\d+|-?\d+', str(results))]
        
    def fetch_integers(self, min_val=1, max_val=20, number=1):
        return self.fetch_randomdotorg(service="integers", num=number, col=1, min=min_val, max=max_val)

    def fetch_pseudorandom_integers(self, min_val=1, max_val=20, number=1):
        try:
            int(self.__seed)
        except ValueError:
            print("The seed must be updated at least once first.")
            self.update_seed()
        output = []
        for i in range(number):
            output.append(random.randint(min_val, max_val))
        self.__latest_results = output
        return output

    def update_seed(self):
        self.__seed = self.fetch_integers(-1000000000, 1000000000)[0]
        random.seed = self.__seed