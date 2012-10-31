#!/usr/bin/env python
import os
import sys
from koala.provider import harvester

def fetch(**kwargs):
    reload(harvester)
    harvester.fetch(**kwargs)
        
def crawl(**kwargs):
    reload(harvester)
    harvester.crawl()        
#we can change this one!
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koala.settings")
    #commnet in the midddle from master
    from django.core.management import execute_from_command_line
    