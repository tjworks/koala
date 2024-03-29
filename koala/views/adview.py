"""
koala.view.adview
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from django.views.decorators.http import require_http_methods
from koala import settings
from koala.application import renderResponse,getContext
from koala.models import Post, Item
from koala.providers import provider
from koala.util.parser import parsePhone
from koala.webutils import getReferer
from myutil import idtool
from myutil.objdict import ObjDict
import json
import logging
from koala.managers.ItemManager import ItemManager

logger = logging.getLogger(__name__)
itemManager = ItemManager()
 
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
        
    return post

def _getPostId(req):
    # get it from referer
    pd = provider.getProvider(req)
    if(pd): post_id = pd.getId()
    if(not post_id):  raise Exception("Missing invitation ID and could not infer from referer %s provider: %s" %(getReferer(req), pd))
    logger.debug("Obtained post id from referer %s" %post_id)
    return post_id
  
def _fillContext(post):
    fetched = post
    ctx = getContext()
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
    
    if('location' in fetched and 'zipCode' in fetched.location):
        ctx.location = ctx['location'] or {}
        ctx.location['zipCode'] = fetched.location['zipCode'].replace('USA-', '')
    
@require_http_methods(["GET", "POST", "HEAD"])
def view(req, post_id=None):
    """
    Buyer view 
    """
    post_id = post_id or _getPostId(req)
    post = _getPost(req, post_id)
    #ctx = getContext()
    _fillContext(post)
    ctx = getContext()
    ctx.template = 'adview.html'
    
    return renderResponse()

@require_http_methods(["GET", "POST", "HEAD"])
def edit(req, post_id=None):
    return activate(req, post_id)

@require_http_methods(["GET", "POST", "HEAD"])
def update(req, item_id=None):
    """
    Update item properties. 
    
    Usage::
    
        /<item_id>/update?name=value&name=value
    
    Example::
    
        /item121107220305425262/update?status=on&price=1990&negotiable=on&location=30303
        
    """
    props = {}
    for key,val in req.REQUEST.iteritems():
        if(key.find('_') != 0): 
            props[key] = val
    itemManager.update(item_id, props)
    #ctx = getContext()
    return renderResponse()

@require_http_methods(["GET", "POST", "HEAD"])
def activate(req, post_id=None):
    """
    This handles the case when seller accepts invitation and clicks the link
    """
    post_id = post_id or _getPostId(req)
    post = _getPost(req, post_id)    
    item = Item.collection.find_one({'post_id': post._id})
    
    if(not item):
        item = Item({'hello':1})
        item._id = idtool.generate("item")
        item.post_id = post._id
        item.save()
        #post.sellervisits = post.sellervisits+1 if ('sellervisits' in post) else 1
        #post.mongo_update()
    item.id = item._id
    post.update(item)
    _fillContext(post)
    ctx = getContext()
    ctx.template = 'adedit.html'
    ctx.item = item
    return renderResponse()
