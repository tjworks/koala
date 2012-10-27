
from django.conf import settings
from myutil.objdict import ObjDict
from koala import settings
from pymongo import Connection
import logging
import os
import sys
import time
import traceback

"""
Dev tools
"""
bm=um=gfm=None
def switch(newname):
    settings.MONGODB_NAME = newname
    initdb()

def initdb():
    pass

    
def index():
    col=getCollection('edge')
    
    print "creating indexes"    
    col.ensure_index('begin')
    col.ensure_index('end')
    #col.ensure_index('author',sparse=True)
    
    #dbcon[settings.MONGODB_NAME].fs.chunks.ensure_index('files_id')
    



def dbinfo():
    print "DB: %s@%s" %(settings.MONGODB_NAME, settings.MONGODB_HOST)
 

if __name__ == '__main__':    
    initdb()
    dbinfo()
    

logger = logging.getLogger(__name__)
__connection = None
__dbase = None

def getConnection():        
        global __connection
        if(not __connection):
            __connection = Connection(settings.MONGODB_HOST, 27017)
        if(not __connection): raise Exception("Cannot get connection")
        return __connection
    
      
    
def getCollection(colName):        
        col =   db()[colName]
        if(not col): raise Exception("Cannot access collection %s" % colName)
        return col
    
def db():        
    return getConnection()[settings.MONGODB_NAME]
        
class ValidationError(Exception):
    pass




def createIndexes():
    pass
    """
    db.network.ensureIndex({ "name" : 1 },{ "name" : "name", "background" : true });
    
    db.system.js.find().forEach(function(u){eval(u._id + " = " + u.value);});
    """
    

    
    
    
    
    
    
    
    
    