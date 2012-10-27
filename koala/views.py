from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods
from koala import settings
from koala import application
from koala.provider import provider
import json,logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST", "HEAD"])
def home(req):
    
    res = checkReferer(req)
    if(res): return res
    
    template = loader.get_template('home.html')
    #ctx = gf_template.get_context(req, {})
    ctx = application.getContext()
    ctx.node_url= settings.NODE_URL or 'http://ONE-CHART.COM:3000'
    
    if('debug' in req.GET and req.GET['debug']):
        ctx.debug_info = renderDebugInfo()
    
    return HttpResponse(template.render(ctx))


def renderDebugInfo():
    import socket
    info ='<div id="debug_footer" style="color:white;border:1px dashed #888;padding:10px;margin:10px"><pre>'
    info += "Server host name: " + socket.gethostname() +"\n"
    info += "Mongo DB: " + settings.MONGODB_HOST +"/"+settings.MONGODB_NAME +"\n"
    info += "Node URL: "  + settings.NODE_URL + "\n"
    info +="</pre></div>"
    return info
    
def checkReferer(req):
    """
    See if user is directed from the ad post by checking the HTTP Referer header
    """
    if(not 'HTTP_REFERER' in req.META):
        logger.debug("No referer") 
        return None
    
    referer = req.META['HTTP_REFERER']
    logger.debug("Referer is %s" %referer) 

    handler = provider.getProvider(referer)
    
    logger.debug("Referer handler is %s" %handler)
    return None