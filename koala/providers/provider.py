from koala import application
from koala.webutils import getReferer
import logging
import re
logger = logging.getLogger(__name__)
def getProvider(request=None, url=None):
    if(not url): url = getReferer(request)
    if(not url): return None
    c = CraigslistProvider(url)
    if(c.accept()): return c 
    """
    m = BaseProvider.__module__
    for attr in dir(m):
        p = getattr(m, attr)
        if(p in BaseProvider.__subclasses__()) :
            pinstance = p(url)
            if(pinstance.accept()): return pinstance
    """
    return None
            

class BaseProvider(object):
    def accept(self, url):
        
        return False;
    
    
class CraigslistProvider(BaseProvider):
    def __init__(self, url=None):
        self.url = url
    def getId(self):
        url = self.url
        if(url.find("craigslist")<0): return None
        m = re.search(r'/(\d{8,})', url)
        if(m): return m.group(1)
        return None
    def accept(self):
        return self.getId()
    def fetch(self, sourceId=None):
        from koala.providers import harvester
        items = harvester.fetch(sourceId)
        return items
        
    