
from django.views.decorators.http import require_http_methods
from koala import settings, application
from koala.models import Post
from koala.util.parser import parsePhone
from koala.webutils import getReferer
from myutil.objdict import ObjDict
from koala.providers import provider
import json
import logging

logger = logging.getLogger(__name__)

def _getPost(req, post_id):
    """
    """    
    pd = provider.CraigslistProvider()
    logger.debug("Provided invite id %s" %post_id)
    post = Post.collection.find_one({'$or': [{'_id': post_id}, {'sourceId':post_id}]})    
    if(not post):  
        # retrieve it from 3taps
        logger.debug("Invite does not exist, fetching")
        post = pd.fetch(post_id)
        if(len(post)>0): 
            logger.debug("fetched from source")
            post=post[0]
        else: 
            logger.debug("fetch failed")        
    if(not post):
        raise Exception("No post found for id %s" %post_id)
    if(not post.fetched):
        logger.debug("Fetching from source")
        raise Exception("Post not fetched yet: %s" %post_id)
        
    return post

def _getPostId(req):
    # get it from referer
    pd = provider.getProvider(req)
    if(pd): post_id = pd.getId()
    if(not post_id):  raise Exception("Missing invitation ID and could not infer from referer %s provider: %s" %(getReferer(req), pd))
    logger.debug("Obtained post id from referer %s" %post_id)
    return post_id
  
def _fillContext(post):
    fetched = post.fetched
    ctx = application.getContext()
    ctx.template = 'howitworks.html'
    ctx.update(fetched)
    
    fetched = ObjDict(fetched)
    ctx.phone = fetched.annotations.phone if fetched.annotations else None
    # phone number
    if(fetched.body):
        parsed = parsePhone(fetched.body)
        if(parsed):  ctx.phone =  parsed
    if(fetched.images and len(fetched.images)>0):
        ctx.default_image = fetched.images[0]
    ctx.phone = ctx.phone or ""
    
@require_http_methods(["GET", "POST", "HEAD"])
def view(req, post_id=None):
    """
    Buyer view 
    """
    post_id = post_id or _getPostId(req)
    post = _getPost(req, post_id)
    #ctx = application.getContext()
    _fillContext(post)
    ctx = application.getContext()
    ctx.template = 'adview.html'
    return application.renderResponse()

@require_http_methods(["GET", "POST", "HEAD"])
def edit(req, post_id=None):
    return activate(req, post_id)
@require_http_methods(["GET", "POST", "HEAD"])
def activate(req, post_id=None):
    """
    This handles the case when seller accepts invitation and clicks the link
    """
    post_id = post_id or _getPostId(req)
    post = _getPost(req, post_id)
    
    post.sellervisits = post.sellervisits+1 if ('sellervisits' in post) else 1
    post.mongo_update()
    
    _fillContext(post)
    ctx = application.getContext()
    ctx.template = 'adedit.html'
    
    return application.renderResponse()
