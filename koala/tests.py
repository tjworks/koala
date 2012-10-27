
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from myutil.fileutil import contentsOfFile
from koala import settings
import json
import os
import unittest
from koala.provider.provider import *

class ProviderTest(TestCase):

    def test_provider(self):
        
        url = "http://atlanta.craigslist.org/atl/bar/3362681592.html"
        p = CraigslistProvider(url)
        self.assertTrue( p.accept() , "URL %s should be accepted by CraigslistProvider" %url)


        url = "http://atlanta.craigslist.org/3362681592"
        p = CraigslistProvider(url)
        self.assertTrue( p.accept() , "URL %s should be accepted by CraigslistProvider" %url)

    def test_harvest(self):
        pass
            #"sourceId": 3362540710,
            