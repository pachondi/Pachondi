from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
# [:index, :show, :new, :create, :edit, :update, :destroy] 


urlpatterns = patterns('',
                        url(r'^groups/', include('app.groups.urls')),
)

urlpatterns += patterns('',
                        url(r'^users/', include('app.users.urls')),                        
)

urlpatterns += patterns('',
                        url(r'^relationships/', include('app.relationships.urls')),                        
)

urlpatterns += patterns('',
                        url(r'^profile/', include('app.profile.urls')),                        
)

urlpatterns += patterns('',
                        url(r'^group_discussions/', include('Pachondi.libs.discussions.urls')),                       

)

urlpatterns += patterns('Pachondi.libs.message.views',
                        (r'group_discussion_messages/$','index'),
                        (r'group_discussion_messages/new$','new',None,'new-group-discussion-message'),
                        (r'group_discussion_messages/create/$','create',None,'create-group-discussion-message'),
                        (r'group_discussion_messages/(?P<message_id>\d+)/edit','edit',None,'edit-group-discussion-message'), # 
                        (r'group_discussion_messages/(?P<message_id>\d+)/update','update',None,'update-group-discussion-message'), 
                        (r'group_discussion_messages/(?P<message_id>\d+)/delete','delete',None,'delete-group-discussion-message'),
                        
                        #(r'group_discussions/(?P<pk>\d+)','show'),
)


"""::
https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/#other-helpers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
"""

#(r'^groups*','index'), # catch all, defaults to index
    # Examples:
    # url(r'^$', 'Pachondi.views.home', name='home'),
    # url(r'^Pachondi/', include('Pachondi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

