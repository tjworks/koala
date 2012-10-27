import logging
import threading
from django.http import HttpResponse
from django.template.context import RequestContext
from django.template import loader

"""
This module is similar to the ApplicationContext in Spring world. The purpose is we can do some simple caching within the thread 

The appContext object is instantiated for each thread  and can be accessed throughout the execution. 
The most important piece of information is the user object(and probably the default face object as well) which is accessed frequently by all parts of the application
"""
appContext = threading.local()
logger = logging.getLogger(__name__)
# returns currently logged in user_id. Raises exception if not logged in
def getCurrentUserId(raiseOnError=True):
	global appContext
	if hasattr(appContext, 'user_id'):
		return appContext.user_id
	elif raiseOnError:
		raise Exception("No user_id in context: is user logged in?")
	else: return None
# returns currently logged in user object. will retrieve from DB if not already exists
def getCurrentUser(raiseOnError=True):
	
	global appContext
	if hasattr(appContext, 'userObj'): 
		#logger.debug("Cache Hit, get user")
		return appContext.userObj
	
	logger.debug("Cache miss, loading user")
	uid = getCurrentUserId(raiseOnError)
	if uid:	
		from gameface.service import UserManager
		appContext.userObj = UserManager.findByUserId(uid)
	if hasattr(appContext, 'userObj'): return appContext.userObj	
	if raiseOnError: raise Exception("Failed to get default user, are you logged in?")	
	return None	

def getContext(req=None):
    """
    Get the current requestcontext object used for template rendering
    Create a new one if not exists
    """
    global appContext
    if hasattr(appContext, 'ctx'): 
        #logger.debug("Cache Hit, get user")
        return appContext.ctx
    
    logger.debug("Creating new context")
    if(not req): raise Exception("Request object must be provided when first time call getContext()")
    appContext.ctx = RequestContext(req, {})
    appContext.ctx.debug = []
    return appContext.ctx

def setUser(userObj):
	appContext.userObj = userObj
	appContext.user_id = userObj.user_id
	
def clearCached():
	if (hasattr(appContext, 'userObj')): delattr(appContext, 'userObj')
	
def clearContext():
	attributes = [attr for attr in appContext.__dict__]
	for attr in attributes:
		delattr(appContext, attr)  
        
def renderResponse():
    #ctx = gf_template.get_context(req, {})
    ctx = getContext()
    template = loader.get_template( ctx.template )
    return HttpResponse(template.render(ctx))