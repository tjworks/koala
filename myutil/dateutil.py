"""
Date utils
"""
from datetime import datetime
import re,time

DATE_SECONDS ='%Y-%m-%d %H:%M:%S'
DATE_MILLIS = '%Y-%m-%d %H:%M:%S.%f'
DATE_UTC = '%Y-%m-%dT%H:%M:%SZ'
DATE_UTC_MILLIS = '%Y-%m-%dT%H:%M:%S.%fZ'
DATE_TIMESTAMP = "%s"
#9 >>> dt.microsecond

def formatTime(tm=None, format=DATE_SECONDS):
    #print("format time, source is %s, %s" %(tm, type(tm)) )
    tm = tm or datetime.utcnow()
    if type(tm) == float: tm= datetime.fromtimestamp(tm)
    if isinstance( tm , basestring):
        dtm = None 
        try: dtm = datetime.strptime(tm, DATE_UTC)
        except: pass        
        if(not dtm):
            try: dtm = datetime.strptime(tm, DATE_SECONDS)
            except: pass
        if(not dtm):
            try: dtm = datetime.strptime(tm, DATE_MILLIS)
            except: pass
        if(not dtm):  raise Exception("Unrecognized date string: %s" %tm)
        tm = dtm 

    #print("tm %s" %tm)
    if(format == DATE_TIMESTAMP):
        return int(time.mktime(tm.timetuple()))
                         
    return tm.strftime(  format )

