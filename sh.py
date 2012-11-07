#!/usr/bin/env python
import os,time
import sys

from threetaps.api import clients, base, models
from koala.providers import harvester
from myutil.objdict import ObjDict

def fetch(**kwargs):
    reload(harvester)
    harvester.fetch(**kwargs)
        
def crawl(**kwargs):
    """
    crawl the 3taps db
    """
    
    """
    sc = clients.SearchAPIClient()
    sc.enableLogging()
    q = ObjDict()
    q.categoryClass='SSSS'
    res = sc.search(q, 1)
    if(True): 
        print res
        return None
    """
    reload(harvester)
    while(True):
        harvester.crawl()
        time.sleep(2)
	break
                
    
#we can change this one!
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koala.settings")
    #commnet in the midddle from master
    from django.core.management import execute_from_command_line
    
