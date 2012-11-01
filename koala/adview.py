
from django.views.decorators.http import require_http_methods
from koala import settings, application
from koala.models import Post
from myutil.objdict import ObjDict
from koala.provider import provider
import json
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST", "HEAD"])
def activate(req, invite_id):
    """
    This handles the case when seller accepts invitation and clicks the link
    """
    if(not invite_id): 
        #check referer
        raise Exception("Missing invitation ID")
    logger.debug("Got invite id %s" %invite_id)
    post = Post.collection.find_one({'$or': [{'_id': invite_id}, {'sourceId':invite_id}]})
    
    if(not post):  
        # retrieve it from 3taps
        pd = provider.CraigslistProvider()
        post = pd.fetch(invite_id)
        if(len(post)>0): post=post[0]
        else: 
            logger.debug("fetch failed")
        logger.debug("fetched from source")
    if(not post):
        raise Exception("No post")
    if(not post.fetched):
        logger.debug("Fetching from source")
        raise Exception("Post not fetched yet: %s" %invite_id)
    
    post.sellervisits = post.sellervisits+1 if ('sellervisits' in post) else 1
    post.mongo_update()
    fetched = post.fetched
    ctx = application.getContext()
    ctx.template = 'howitworks.html'
    ctx.update(fetched)
    
    fetched = ObjDict(fetched)
    ctx.phone = fetched.annotations.phone if fetched.annotations else None
    # phone number
    if(fetched.body):
        txt = fetched.body
        txt = txt.replace('-', '').lower().replace('.', '')
        reps = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "zero":0}
        for key,num in reps.iteritems():
            txt=txt.replace(key, "%s" %num)
        txt = txt.replace(' ', '')
        import re
        #pat = re.compile(r"(\s*one\s*|\s*two\s*|\s*three\s*|\s*four\s*|\s*five\s*|\s*six\s*|\s*seven\s*|\s*eight\s*|\s*nine\s*|\s*zero\s*|\s*[0-9]\s*){10}", re.IGNORECASE)
        pat = re.compile("[2-9][0-9]{9}")
        matcher = pat.search(txt)
        print("matcher %s --> %s" %(matcher, txt) )
        if(matcher):
            ctx.phone = "" + matcher.group(0)
    if(fetched.images and len(fetched.images)>0):
        ctx.default_image = fetched.images[0]
    
     
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