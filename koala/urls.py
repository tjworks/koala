from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    
    url('^docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'docs/_build/html'}),
    url('^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    
    url(r'^pages/(?P<pagename>.*)$', 'koala.views.main.serve'),
    # search/proxy
    url(r'^(?P<post_id>.*)/edit/?$', 'koala.views.adview.edit'),
    url(r'^(?P<post_id>.*?)/?activate/?$', 'koala.views.adview.activate'),
    url(r'^(?P<post_id>.*?)/?view/?$', 'koala.views.adview.view'),
    url(r'^(?P<item_id>.*)/update/?$', 'koala.views.adview.update'),
    
    #url(r'^activate/(?P<post_id>.*)$', 'koala.views.adview.activate'),    
    #url(r'^view/(?P<post_id>.*)$', 'koala.views.adview.view'),    
     
    #url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    #url(r'^(?P<path>.*.(css|js|png|gif|swf|jpg|html|htm|pdf|csv|json))$', 'django.views.static.serve', {'document_root': 'static'}),

    # url(r'^koala/', include('koala.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Home page
    url(r'^$', 'koala.views.main.home'),

    url(r'^howto$', 'koala.views.home'),
)

"""
    url(r'^(?P<path>.*.js)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^(?P<path>.*.png)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^(?P<path>.*.gif)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^(?P<path>.*.swf)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^(?P<path>.*.jpg)$', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^(?P<path>.*.html)$', 'django.views.static.serve', {'document_root': 'static'}),
    """

