from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods
from koala import application, settings
from koala.providers import provider
from koala.webutils import checkReferer
import json
import logging

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
    