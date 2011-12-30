from django.conf.urls.defaults import *
from django.conf import settings

import lib.django_cron
lib.django_cron.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^beatwrit/', include('beatwrit.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #main pages
    (r'^[/]?$', 'main.views.home'),
    (r'^browse$', 'main.views.browse'),
    (r'^joinbrowse$', 'main.views.joinbrowse'),
    
    (r'^authors/(?P<bwuid>[\d]{1,12})$', 'main.views.author'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/settings$', 'main.views.usersettings'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/addcircle$', 'main.views.addcircle'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/remcircle$', 'main.views.removecircle'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/econf$', 'main.views.emailconfirm'),

    (r'^profile$', 'main.views.myprofile'),
    (r'^writs/(?P<writid>[\d]+)[/]?$', 'main.views.writview'),
    (r'^writs/(?P<writid>[\d]+)/join$', 'main.views.writjoin'),
    (r'^writs/new', 'main.views.writcreate'),
    (r'^writs/post', 'main.views.writpost'),
    (r'^authors/new', 'main.views.usercreate'),
    
    #user auth
    (r'^login[/]?$', 'main.views.loginview'),
    (r'^logout[/]?$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^_l/(?P<uid>[\d]+)/(?P<token_no>[\d]+)$', 'main.views.autologin'),

    #ajax/json
    (r'^authors/(?P<bwuid>[\d]{1,12})/activewrits$', 'main.ajaxviews.active_writs'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/compwrits$', 'main.ajaxviews.completed_writs'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/circwrits$', 'main.ajaxviews.circle_writs'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/commwrits$', 'main.ajaxviews.community_writs'),
    
    #ajax/html
    (r'^authors/(?P<bwuid>[\d]{1,12})/h_activewrits$', 'main.htmlviews.active_writs'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/h_compwrits$', 'main.htmlviews.completed_writs'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/h_circwrits$', 'main.htmlviews.circle_writs'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/h_commwrits$', 'main.htmlviews.community_writs'),
    
    #other
    (r'^test/error[/]?$', 'main.views.oops'),
    (r'^oops/?$', 'main.views.oops'),
    (r'^message/?$', 'main.views.fullmessage'),



    #(testing pages)
    (r'^writs/(?P<writid>[\d]{1,12})/delete$', 'main.views.writdelete'),
    (r'^writs/(?P<writid>[\d]{1,12})/parts$', 'main.views.writuserordertest'),
    (r'^writs/(?P<writid>[\d]{1,12})/additions$', 'main.views.writadditionstest'),
    (r'^writs/(?P<writid>[\d]{1,12})/settings$', 'main.views.writsettingstest'),
    (r'^writs/$', 'main.views.writbrowse'),
    (r'^nods/?$', 'main.views.nodsquery'),
    (r'^authors/(?P<bwuid>[\d]{1,12})/friends$', 'main.views.authorsfriendstest'),
    
    (r'^writs/(?P<writid>[\d]+)/magic$', 'main.views.writview_autologin'),
    (r'^writs/(?P<writid>[\d]+)/magicpost$', 'main.views.writview_autologinpost'),
)



if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('',
    
        (r'^files/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_DOC_ROOT}),
)
