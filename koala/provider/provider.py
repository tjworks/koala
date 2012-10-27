from koala import application
import logging,re
logger = logging.getLogger(__name__)

def getProvider(url):
    m = BaseProvider.__module__
    for attr in dir(m):
        p = getattr(m, attr)
        if(p in BaseProvider.__subclasses__()) :
            pinstance = p(referer)
            if(pinstance.accept()): return pinstance 
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
    