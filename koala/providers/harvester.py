from koala import application
import logging,re,requests, json,uuid
from koala.models import Post
from myutil.dateutil import *
import pymongo

logger = logging.getLogger(__name__)
PAGE_SIZE = 100
#threeTaps = 'http://3taps.net/search?authToken=4a207d226ba34e5aab23c022157f29a7&source=CRAIG&rpp=100&metroCode=USA-ATL&heading=MINI Cooper&annotations={source_subcat:cto}'
threeTaps = 'http://3taps.net/search?authToken=4a207d226ba34e5aab23c022157f29a7&source=CRAIG&metroCode=USA-ATL&categoryClass=SSSS&rpp=1&'
def fetch(sourceId=None):
    url = threeTaps
    if(sourceId): url = "%s&sourceId=%s" %(url, sourceId)
    else: url = "%s&annotations={source_subcat:cta|cto}"
    ret = []
    _fetch(url, ret)
    return ret

def _fetch(url, ret):
    # first get the count
    obj = _load(url)
    source = "clst"
    logger.debug( "Total results %s" %(  obj['numResults']) )
    
    # default rpp size 100
    total = obj['numResults']
    pageno = 0
    import math
    while (  pageno < math.ceil(  float(total)/PAGE_SIZE ) ):  # page no less than total page no, 0 based
        #page 0 already loaded, start from 1
        logger.debug( "Loading page %s" %(pageno))
        theurl = "%s&rpp=%s&page=%s" %(url, PAGE_SIZE, pageno)
        obj = _load(theurl)
        if(not obj):
            logger.error("Failed to load!")
            continue
        skipped=0
        for entry in obj['results']:
            if(not 'sourceId' in entry):
                logger.error("Invalid entry, missing sourceId: %s" %entry)
                continue
            p = convert(entry)
            if(p):
                logger.debug("Adding post: %s" %entry['sourceUrl'])
                p.save()
                ret.append(p)
            else:
                skipped = skipped+1
                logger.debug("Skipping post, already exists: %s" %entry['sourceUrl'])
        pageno = pageno +1
        if(skipped == len(obj['results'])):
            logger.debug("This request was all skipped, we must have the data from this point on, abort")
            break        
        logger.debug("Sleeping a little")
        time.sleep(10)
    return ret
def _load(url):
    logger.debug("Fetching %s" %url)
    r = requests.get(url)
    if (r.status_code != 200):
        logger.error("Failed to load request %s: status %s" %(url, r.status_code))
        return None
    
    from django.utils.encoding import smart_str    
    content = smart_str(r.text)
    obj = json.loads(content)
    return obj
def convert(entry):
    """
    Convert fetched data into model
    """
    #if('annotations' in entry and 'source_subcat' in entry['annotations'] and entry['annotations']['source_subcat']== 'cta|cto'):
    source = "clst"
    _id =  "post%s%s" % (source, entry['sourceId'])
    p = Post.collection.find_one({'_id': _id})
    if(not p):        
        p=Post()
        if('html' in entry):   del entry['html']            
        p.sourceId = "%s" %(entry['sourceId'])
        p.fetched = entry
        p.ptm = formatTime( entry['postingTimestamp'] )
        p.ctm = formatTime()
        p._id = _id
        return p
    else: 
        return None

def crawl():
    """
    - Query for all for sale items from 10/1, in USA-ATL
    - Find the latest time stamp
    - Query from that time stamp + 10 minutes, sleep 1 minute
    """
    start = "2012-10-16 00:00:00"
    cursor = Post.collection.find({}, {'ptm':1}).sort('ptm', pymongo.DESCENDING).limit(1)
    if(cursor and cursor.count()>0):
        d = cursor[0]
        if('ptm' in d): start= d['ptm']
        print "Starting time: %s" %start
    else:
        logger.debug("No record, starting from 10/1")  
    logger.info("Requesting posts from %s  " %start)
    start = formatTime(start, DATE_TIMESTAMP) 
    end = start + 60 * 60 * 24 # one day      
    url = "%s&start=%s&end=%s&" %(threeTaps, start, end)
    url = threeTaps    
    ret = []
    _fetch(url, ret)
    logger.info("Harvested %s items" %(len(ret)))
     
"""
{
            "accountId": 1,
            "annotations": {
                "source_account": "q3fdh-3362681592@sale.craigslist.org",
                "source_neighborhood": "downtown",
                "phone": "3362681592",
                "source_continent": "usa",
                "source_loc": "atlanta",
                "source_cat": "sss",
                "source_subloc": "atl",
                "year": "2012",
                "source_state": "georgia",
                "source_subcat": "bar"
            },
            "body": "Im native Chinese speaker looking for a native Spanish speaker to exchange language lessons or just casual conversation Im fluent in English and elementary beginner in Spanish     Location Downtown  its NOT ok to contact this poster with services or other commercial interests    PostingID 3362681592     Copyright copy 2012 craigslist inc  terms of use  privacy policy  feedback forum  ",
            "category": "SBAR",
            "categoryClass": "SSSS",
            "categoryClassName": "For Sale",
            "categoryName": "Barters",
            "currency": "USD",
            "expirationTimestamp": "2012-12-08T22:45:00Z",
            "flags": 1,
            "hasImage": false,
            "heading": "Language Exchange  Downtown",
            "html": "PCFET0NUWVBFIGh0bWwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMDEgVHJhbnNpdGlvbmFsLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL1RSL2h0bWw0L2xvb3NlLmR0ZCI+CjxodG1sPgo8aGVhZD4KCTx0aXRsZT5MYW5ndWFnZSBFeGNoYW5nZSAtIERvd250b3duPC90aXRsZT4KCTxtZXRhIG5hbWU9InJvYm90cyIgY29udGVudD0iTk9BUkNISVZFLE5PRk9MTE9XIj4KCTxsaW5rIHR5cGU9InRleHQvY3NzIiByZWw9InN0eWxlc2hlZXQiIG1lZGlhPSJhbGwiIGhyZWY9Imh0dHA6Ly93d3cuY3JhaWdzbGlzdC5vcmcvc3R5bGVzL2NyYWlnc2xpc3QuY3NzP3Y9Y2RlZDBkYzA3MDM2OWUwNGU1ZDFlNGFhYWIxZTNlZjMiPgoJCiAgICA8IS0tW2lmIGx0ZSBJRSA4XT4KCQkKICAgIDwhW2VuZGlmXS0tPgogICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9InVzZXItc2NhbGFibGU9MTsiPgo8L2hlYWQ+Cgo8Ym9keSBjbGFzcz0icG9zdGluZyI+Cgo8ZGl2IGNsYXNzPSJiY2hlYWQiPgo8YSBpZD0iZWYiIGhyZWY9Imh0dHBzOi8vYWNjb3VudHMuY3JhaWdzbGlzdC5vcmcvZWFmP3Bvc3RpbmdJRD0zMzYyNjgxNTkyJmFtcDt0b2tlbj1VMkZzZEdWa1gxODNOVGsxTnpVNU5lYWd1a1RkQkIyekVjUm9TM3RXWDlKSnhZSmxfbFZkUmo0ZVRBQ3JzZFh2N3laRDMxRmdreENLZDkxdURrdDlRYkxKOFUzcWRxQWgiPmVtYWlsIHRoaXMgcG9zdGluZyB0byBhIGZyaWVuZDwvYT4gPGEgaHJlZj0iaHR0cDovL2F0bGFudGEuY3JhaWdzbGlzdC5vcmcvIj5hdGxhbnRhIGNyYWlnc2xpc3Q8L2E+ICZndDsgPGEgaHJlZj0iaHR0cDovL2F0bGFudGEuY3JhaWdzbGlzdC5vcmcvYXRsLyI+YXRsYW50YTwvYT4gJmd0OyAgPGEgaHJlZj0iaHR0cDovL2F0bGFudGEuY3JhaWdzbGlzdC5vcmcvYXRsL3Nzcy8iPmZvciBzYWxlIC8gd2FudGVkPC9hPiAmZ3Q7IDxhIGhyZWY9Imh0dHA6Ly9hdGxhbnRhLmNyYWlnc2xpc3Qub3JnL2F0bC9iYXIvIj5iYXJ0ZXI8L2E+CjwvZGl2PgoJPGRpdiBpZD0iZmxhZ3MiPgoJCTxkaXYgaWQ9ImZsYWdNc2ciPgoJCQlwbGVhc2UgZmxhZyB3aXRoIGNhcmU6IDxhIGhyZWY9Imh0dHA6Ly93d3cuY3JhaWdzbGlzdC5vcmcvYWJvdXQvaGVscC9mbGFnc19hbmRfY29tbXVuaXR5X21vZGVyYXRpb24iPls/XTwvYT4KCQk8L2Rpdj4KCQk8ZGl2IGlkPSJmbGFnQ2hvb3NlciI+CgkJCTxicj4KCQkJPGEgY2xhc3M9ImZsIiBpZD0iZmxhZzE2IiBocmVmPSIvZmxhZy8/ZmxhZ0NvZGU9MTYmYW1wO3Bvc3RpbmdJRD0zMzYyNjgxNTkyIgoJCQkJdGl0bGU9Ildyb25nIGNhdGVnb3J5LCB3cm9uZyBzaXRlLCBkaXNjdXNzZXMgYW5vdGhlciBwb3N0LCBvciBvdGhlcndpc2UgbWlzcGxhY2VkIj4KCQkJCW1pc2NhdGVnb3JpemVkPC9hPgoJCQk8YnI+CgoJCQk8YSBjbGFzcz0iZmwiIGlkPSJmbGFnMjgiIGhyZWY9Ii9mbGFnLz9mbGFnQ29kZT0yOCZhbXA7cG9zdGluZ0lEPTMzNjI2ODE1OTIiCgkJCQl0aXRsZT0iVmlvbGF0ZXMgY3JhaWdzbGlzdCBUZXJtcyBPZiBVc2Ugb3Igb3RoZXIgcG9zdGVkIGd1aWRlbGluZXMiPgoJCQkJcHJvaGliaXRlZDwvYT4KCQkJPGJyPgoKCQkJPGEgY2xhc3M9ImZsIiBpZD0iZmxhZzE1IiBocmVmPSIvZmxhZy8/ZmxhZ0NvZGU9MTUmYW1wO3Bvc3RpbmdJRD0zMzYyNjgxNTkyIgoJCQkJdGl0bGU9IlBvc3RlZCB0b28gZnJlcXVlbnRseSwgaW4gbXVsdGlwbGUgY2l0aWVzL2NhdGVnb3JpZXMsIG9yIGlzIHRvbyBjb21tZXJjaWFsIj4KCQkJCXNwYW0vb3ZlcnBvc3Q8L2E+CgkJCTxicj4KCgkJCTxhIGNsYXNzPSJmbCIgaWQ9ImZsYWc5IiBocmVmPSIvZmxhZy8/ZmxhZ0NvZGU9OSZhbXA7cG9zdGluZ0lEPTMzNjI2ODE1OTIiCgkJCQl0aXRsZT0iU2hvdWxkIGJlIGNvbnNpZGVyZWQgZm9yIGluY2x1c2lvbiBpbiB0aGUgQmVzdC1PZi1DcmFpZ3NsaXN0Ij4KCQkJCWJlc3Qgb2YgY3JhaWdzbGlzdDwvYT4KCQkJPGJyPgoJCTwvZGl2PgoJPC9kaXY+Cgo8ZGl2IGlkPSJ0c2IiPgoJCQk8ZW0+QXZvaWQgc2NhbXMgYW5kIGZyYXVkIGJ5IGRlYWxpbmcgbG9jYWxseSE8L2VtPiBCZXdhcmUgYW55IGRlYWwgaW52b2x2aW5nIFdlc3Rlcm4gVW5pb24sIE1vbmV5Z3JhbSwgd2lyZSB0cmFuc2ZlciwgY2FzaGllciBjaGVjaywgbW9uZXkgb3JkZXIsIHNoaXBwaW5nLCBlc2Nyb3csIG9yIGFueSBwcm9taXNlIG9mIHRyYW5zYWN0aW9uIHByb3RlY3Rpb24vY2VydGlmaWNhdGlvbi9ndWFyYW50ZWUuIDxhIGhyZWY9Imh0dHA6Ly93d3cuY3JhaWdzbGlzdC5vcmcvYWJvdXQvc2NhbXMiPk1vcmUgaW5mbzwvYT48L2Rpdj4KPGgyPkxhbmd1YWdlIEV4Y2hhbmdlIC0gRG93bnRvd24gKERvd250b3duKTwvaDI+Cjxocj4KPHNwYW4gY2xhc3M9InBvc3RpbmdkYXRlIj5EYXRlOiAyMDEyLTEwLTI0LCAgNjo0NVBNIEVEVDwvc3Bhbj48YnI+CgoJCTxzY3JpcHQgdHlwZT0idGV4dC9qYXZhc2NyaXB0Ij48IS0tCgkJCXZhciBpc1ByZXZpZXcgPSAiIjsKdmFyIHBvc3RpbmdUaXRsZSA9ICJMYW5ndWFnZSBFeGNoYW5nZSAtIERvd250b3duIChEb3dudG93bikiOwp2YXIgYmVzdE9mID0gIiI7CnZhciBwb3N0aW5nVVJMID0gImh0dHAlM0ElMkYlMkZhdGxhbnRhLmNyYWlnc2xpc3Qub3JnJTJGYXRsJTJGYmFyJTJGMzM2MjY4MTU5Mi5odG1sIjsKdmFyIGRpc3BsYXlFbWFpbCA9ICJxM2ZkaC0zMzYyNjgxNTkyQHNhbGUuY3JhaWdzbGlzdC5vcmciOwoKCQktLT48L3NjcmlwdD4KCQoKPGJ1dHRvbiBpZD0icmVwbHlfYnV0dG9uIj5SZXBseSB0byB0aGlzIHBvc3Q8L2J1dHRvbj4KCjxzcGFuIGlkPSJyZXBseXRleHQiPlJlcGx5IHRvOjwvc3Bhbj4gPHNtYWxsPjxhIGhyZWY9Im1haWx0bzpxM2ZkaC0zMzYyNjgxNTkyQHNhbGUuY3JhaWdzbGlzdC5vcmc/c3ViamVjdD1MYW5ndWFnZSUyMEV4Y2hhbmdlJTIwLSUyMERvd250b3duJTIwKERvd250b3duKSZhbXA7Ym9keT0lMEElMEFodHRwJTNBJTJGJTJGYXRsYW50YS5jcmFpZ3NsaXN0Lm9yZyUyRmF0bCUyRmJhciUyRjMzNjI2ODE1OTIuaHRtbCUwQSI+cTNmZGgtMzM2MjY4MTU5MkBzYWxlLmNyYWlnc2xpc3Qub3JnPC9hPjwvc21hbGw+IDxzdXA+WzxhIGhyZWY9Imh0dHA6Ly93d3cuY3JhaWdzbGlzdC5vcmcvYWJvdXQvaGVscC9yZXBseWluZ190b19wb3N0cyIgdGFyZ2V0PSJfYmxhbmsiPkVycm9ycyB3aGVuIHJlcGx5aW5nIHRvIGFkcz88L2E+XTwvc3VwPgo8ZGl2IGlkPSJyZXR1cm5lbWFpbCI+IDwvZGl2PgoKCjxocj4KPGJyPgo8ZGl2IGlkPSJ1c2VyYm9keSI+CkknbSBuYXRpdmUgQ2hpbmVzZSBzcGVha2VyIGxvb2tpbmcgZm9yIGEgbmF0aXZlIFNwYW5pc2ggc3BlYWtlciB0byBleGNoYW5nZSBsYW5ndWFnZSBsZXNzb25zIG9yIGp1c3QgY2FzdWFsIGNvbnZlcnNhdGlvbi4gSSdtIGZsdWVudCBpbiBFbmdsaXNoIGFuZCBlbGVtZW50YXJ5IGJlZ2lubmVyIGluIFNwYW5pc2g8IS0tIFNUQVJUIENMVEFHUyAtLT4KPGJyPgo8dWwgY2xhc3M9ImJsdXJicyI+CjxsaT4gPCEtLSBDTFRBRyBHZW9ncmFwaGljQXJlYT1Eb3dudG93biAtLT5Mb2NhdGlvbjogRG93bnRvd248L2xpPgo8bGk+aXQncyBOT1Qgb2sgdG8gY29udGFjdCB0aGlzIHBvc3RlciB3aXRoIHNlcnZpY2VzIG9yIG90aGVyIGNvbW1lcmNpYWwgaW50ZXJlc3RzPC9saT48L3VsPgo8IS0tIEVORCBDTFRBR1MgLS0+CjwvZGl2PgoKPHNwYW4gY2xhc3M9InBvc3RpbmdpZHRleHQiPlBvc3RpbmdJRDogMzM2MjY4MTU5Mjxicj48L3NwYW4+Cgo8YnI+Cgo8aHI+Cjx1bCBjbGFzcz0iY2xmb290ZXIiPgoJPGxpPkNvcHlyaWdodCAmY29weTsgMjAxMiBjcmFpZ3NsaXN0LCBpbmMuPC9saT4KCTxsaT48YSBocmVmPSJodHRwOi8vd3d3LmNyYWlnc2xpc3Qub3JnL2Fib3V0L3Rlcm1zLm9mLnVzZSI+dGVybXMgb2YgdXNlPC9hPjwvbGk+Cgk8bGk+PGEgaHJlZj0iaHR0cDovL3d3dy5jcmFpZ3NsaXN0Lm9yZy9hYm91dC9wcml2YWN5X3BvbGljeSI+cHJpdmFjeSBwb2xpY3k8L2E+PC9saT4KCTxsaT48YSBocmVmPSIvZm9ydW1zLz9mb3J1bUlEPTgiPmZlZWRiYWNrIGZvcnVtPC9hPjwvbGk+CjwvdWw+CgoKCQk8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCI+PCEtLQoJCQl2YXIgcGFnZXR5cGUgPSAicG9zdGluZyI7CnZhciBwSUQgPSAiMzM2MjY4MTU5MiI7CnZhciB3d3d1cmwgPSAiaHR0cDovL3d3dy5jcmFpZ3NsaXN0Lm9yZyI7CgoJCS0tPjwvc2NyaXB0PgoJCjxzY3JpcHQgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Imh0dHA6Ly93d3cuY3JhaWdzbGlzdC5vcmcvanMvanF1ZXJ5LTEuNy4yLm1pbi5qcz92PTBhYmU3YmQ5OTRjNDFhOGQ3Y2U0ZTUxYzIxY2NkOTdiIj48L3NjcmlwdD4KPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iaHR0cDovL3d3dy5jcmFpZ3NsaXN0Lm9yZy9qcy9wb3N0aW5ncy5qcz92PTQyZDVmNTQ5YjI4YzQ4YTBlZTczYzMxYzQ1YTZhZTcwIj48L3NjcmlwdD4KPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iaHR0cDovL3d3dy5jcmFpZ3NsaXN0Lm9yZy9qcy9mb3JtYXRzLmpzP3Y9MWNlODI3MTg5NTU3ODBkMWMxMzlkOTY4N2E5MDM0MTIiPjwvc2NyaXB0PgoKCgoKPCEtLSBXaXJlZE1pbmRzIGVNZXRyaWNzIHRyYWNraW5nIHdpdGggRW50ZXJwcmlzZSBFZGl0aW9uIFY1LjQgU1RBUlQgLS0+CjxzY3JpcHQgdHlwZT0ndGV4dC9qYXZhc2NyaXB0JyBzcmM9J2h0dHBzOi8vY291bnQuY2FycmllcnpvbmUuY29tL2FwcC9jb3VudF9zZXJ2ZXIvY291bnQuanMnPjwvc2NyaXB0Pgo8c2NyaXB0IHR5cGU9J3RleHQvamF2YXNjcmlwdCc+PCEtLQp3bV9jdXN0bnVtPSc5NDE0OGM1MzhmYTI0ZTkxJzsKd21fcGFnZV9uYW1lPScxLnBocCc7CndtX2dyb3VwX25hbWU9Jy9zZXJ2aWNlcy93ZWJwYWdlcy9kL2kvZGlzdHJpY3Rnb2xkLmNvbS9wdWJsaWMnOwp3bV9jYW1wYWlnbl9rZXk9J2NhbXBhaWduX2lkJzsKd21fdHJhY2tfYWx0PScnOwp3aXJlZG1pbmRzLmNvdW50KCk7Ci8vIC0tPgo8L3NjcmlwdD4KPCEtLSBXaXJlZE1pbmRzIGVNZXRyaWNzIHRyYWNraW5nIHdpdGggRW50ZXJwcmlzZSBFZGl0aW9uIFY1LjQgRU5EIC0tPgo8IS0tIFdpcmVkTWluZHMgUGl3aWsgdHJhY2tpbmcgU1RBUlQgLS0+CjxzY3JpcHQgdHlwZT0ndGV4dC9qYXZhc2NyaXB0JyBzcmM9J2h0dHBzOi8vY291bnQuY2FycmllcnpvbmUuY29tL2FwcC9jb3VudF9zZXJ2ZXIvY291bnRfcGl3aWsuanMnPjwvc2NyaXB0Pgo8c2NyaXB0IHR5cGU9J3RleHQvamF2YXNjcmlwdCc+PCEtLQp3bV9jdXN0bnVtPSc5NDE0OGM1MzhmYTI0ZTkxJzsKd21fcGFnZV9uYW1lPScxLnBocCc7CndtX2dyb3VwX25hbWU9Jy9zZXJ2aWNlcy93ZWJwYWdlcy9kL2kvZGlzdHJpY3Rnb2xkLmNvbS9wdWJsaWMnOwp3bV9jYW1wYWlnbl9rZXk9J2NhbXBhaWduX2lkJzsKd21fdHJhY2tfYWx0PScnOwp3aXJlZG1pbmRzX3B3LmNvdW50KCk7Ci8vIC0tPgo8L3NjcmlwdD4KPCEtLSBXaXJlZE1pbmRzIFBpd2lrIHRyYWNraW5nIEVORCAtLT4KPC9ib2R5Pgo8L2h0bWw+CgoKCg==",
            "id": 74548217,
            "images": [],
            "immortal": false,
            "indexed": "2012-10-24T23:42:31Z",
            "language": "EN",
            "location": {
                "latitude": 33.749,
                "longitude": -84.38798,
                "accuracy": 4,
                "countryCode": "USA",
                "regionCode": "USA-ATL-ATL",
                "stateCode": "USA-GA",
                "metroCode": "USA-ATL",
                "countyCode": "USA-GA-FUL",
                "cityCode": "USA-ATL-ATA",
                "localityCode": "USA-ATL-DOW",
                "zipCode": "USA-30303"
            },
            "postingTimestamp": "2012-10-24T22:45:00Z",
            "price": 0,
            "source": "CRAIG",
            "sourceId": 3362681592,
            "sourceUrl": "http://atlanta.craigslist.org/atl/bar/3362681592.html"
        },
        {
        """