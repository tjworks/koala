"""
proxy for client side JS due to the xsite security limitation
"""
from django.http import HttpResponse
import json,logging
logger = logging.getLogger(__name__)
class SmartResponse(HttpResponse):
	'''Like an HttpResponse, but encodes the data as JSON.
	The file-like operations probably won't do what you want.'''
	def __init__(self, obj, request, **kw):		
		mimetype="text/html"
		if(request and request.path_info.find('.json')>0):
			#json format
			if (isinstance(obj, Exception)):
				obj = {'error': "%s" %obj}
			obj = json.dumps(obj)
			mimetype = 'application/json'
		super(SmartResponse, self).__init__(obj, mimetype=mimetype, **kw)
		

def getReferer(req):
	"""
	See if user is directed from the ad post by checking the HTTP Referer header
	"""
	if(not 'HTTP_REFERER' in req.META):
		logger.debug("No referer") 
		return None
	
	referer = req.META['HTTP_REFERER']
	logger.debug("Referer is %s" %referer) 
	return referer
	#handler = provider.getProvider(referer)
	
	#logger.debug("Referer handler is %s" %handler)
	#return None