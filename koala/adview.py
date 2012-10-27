
from django.views.decorators.http import require_http_methods
from koala import settings,application
from koala.provider import provider
from koala.models import Post
import json,logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST", "HEAD"])
def activate(req, invite_id):
    """
    This handles the case when seller accepts invitation and clicks the link
    """
    if(not invite_id): raise Exception("Missing invitation ID")
        
    post = Post.collection.find_one({'_id': invite_id})
    
    if(not post):  raise Exception("Post not found: %s" %invite_id)
    
    if(not post.fetched):
        logger.debug("Fetching from source")
    
    post.sellervisits = post.sellervisits+1 if ('sellervisits' in post) else 1
    post.mongo_update()
    
    ctx = application.getContext()
    ctx.template = 'adedit.html'
    ctx.update(post)
     
    return application.renderResponse()

 
    
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