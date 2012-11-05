from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods
from koala import application, settings
import json
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST", "HEAD"])
def home(req):
     
    
    template = loader.get_template('howitworks.html')
    #ctx = gf_template.get_context(req, {})
    ctx = application.getContext()
    
    if('debug' in req.GET and req.GET['debug']):
        ctx.debug_info = renderDebugInfo()
    
    return HttpResponse(template.render(ctx))

def serve(req, pagename=None):
    """
    Serve static pages    
    """
    pagename = pagename or 'home.html'
    template = loader.get_template(pagename)
    #ctx = gf_template.get_context(req, {})
    ctx = application.getContext()
    
    
    return HttpResponse(template.render(ctx))
    

def renderDebugInfo():
    import socket
    info ='<div id="debug_footer" style="color:white;border:1px dashed #888;padding:10px;margin:10px"><pre>'
    info += "Server host name: " + socket.gethostname() +"\n"
    info += "Mongo DB: " + settings.MONGODB_HOST +"/"+settings.MONGODB_NAME +"\n"
    info += "Node URL: "  + settings.NODE_URL + "\n"
    info +="</pre></div>"
    return info
    