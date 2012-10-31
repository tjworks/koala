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

def getTime(tm=None, format=DATE_SECONDS):
    tm = tm or datetime.utcnow()
    if type(tm) == float: tm= datetime.fromtimestamp(tm)
    if type(tm) == str: 
        try: tm = datetime.strptime(tm, DATE_UTC)
        except: pass        
        if(not tm):
            try: tm = datetime.strptime(tm, DATE_SECONDS)
            except: pass
        if(not tm):
            try: tm = datetime.strptime(tm, DATE_MILLIS)
            except: pass
                
        raise "Unrecognized date string: %s" %tm 

    if(format == DATE_TIMESTAMP):
        return int(time.mktime(tm.timetuple()))
                         
    return tm.strftime(  format )