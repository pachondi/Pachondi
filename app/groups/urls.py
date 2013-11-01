from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required
from app.groups.views import GroupCreate, GroupUpdate


urlpatterns = patterns('app.groups.views',
                       (r'^$','show_all',None,'show-group-all'), # show all group
                       (r'^create$',login_required(GroupCreate.as_view()),None,'group-create'),
                       (r'^(?P<pk>\d+)/edit',login_required(GroupUpdate.as_view()),None,'group-update'),
                       (r'^(?P<group_id>\d+)','show_group',None,'group-show'),
                       )

"""urlpatterns = patterns('app.groups.views',
                       #(r'^$','index'), # show all group
                       (r'^$','show_all',None,'show-group-all'), # show all group
                       (r'^create$',login_required(GroupCreate.as_view()),None,'group-create'),
                       (r'^(?P<pk>\d+)/edit',login_required(GroupUpdate.as_view()),None,'group-update'),
                       #(r'^(?P<group_id>\d+)/edit','edit'), # to edit a group
                       #(r'^edit/(?P<group_id>\d+)','edit'), # to edit a group
                       (r'^(?P<group_id>\d+)/update','update'), # post after edit
                       #(r'^update/(?P<group_id>\d+)','update'), # post after edit
                       (r'^(?P<group_id>\d+)/delete','delete'), # to delete a group
                       #(r'^delete/(?P<group_id>\d+)','delete'), # to delete a group
                       (r'^(?P<group_id>\d+)/destroy','destroy'), # to post after delete
                       #(r'^destroy/(?P<group_id>\d+)','destroy'), # to post after delete
                       #(r'^(?P<group_id>\d+)','show'),
                       (r'^(?P<group_id>\d+)','show_group',None,'group-show'),
                       #(r'^new$','new'),  # to create a group
                       #(r'^create/$','create'),  # post after create
                       )
"""