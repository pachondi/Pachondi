from app.relationships.views import relationship_redirect, RelationshipListView, request_connect, decline_connect, \
    accept_connect, delete_request_connect
from django.conf.urls import patterns, url

urlpatterns = patterns('app.relationships.views',
   (r'^request/(?P<uid>\d+)$', request_connect),
   (r'^deleterequest/(?P<uid>\d+)$', delete_request_connect),
   (r'^accept/(?P<uid>\d+)$', accept_connect),
   (r'^reject/(?P<uid>\d+)$', decline_connect),
    url(r'^$', relationship_redirect, name='relationship_list_base'),
    url(r'^(?P<email>[\w.@+-]+)/(?:(?P<status_slug>[\w-]+)/)?$', RelationshipListView.as_view(template_name='relationships/relationship_list.html'), name='relationship_list'),
    url(r'^add/(?P<email>[\w.@+-]+)/(?P<status_slug>[\w-]+)/$', 'relationship_handler', {'add': True}, name='relationship_add'),
    url(r'^remove/(?P<email>[\w.@+-]+)/(?P<status_slug>[\w-]+)/$', 'relationship_handler', {'add': False}, name='relationship_remove'),
)
