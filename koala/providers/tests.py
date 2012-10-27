
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

class ProviderTest(TestCase):

    def test_savenetwork(self):
        
        url = "http://atlanta.craigslist.org/atl/bar/3362681592.html"
        self.assertTrue(url.find("http")==0)

