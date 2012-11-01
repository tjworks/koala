"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from myutil.dateutil import *
import time,datetime
import unittest


class UtilTest(TestCase):

    def test_xml2json(self):
        pass
 
        
class DateTest(TestCase):
    def test_gettime(self):
        tm='2001-01-01 00:11:22'
        now = time.time()
        tm= formatTime(now, DATE_SECONDS)
        self.assertTrue( len(tm) == 19)
        print ("tm is %s" %tm)
        tm = formatTime(datetime.datetime.now(), DATE_TIMESTAMP)
        self.assertTrue(type(tm) == int)
        print ("tm is %s" %tm)
        
        
        