from django.conf.urls import patterns


urlpatterns = patterns('app.groups.views',
                       #(r'^$','index'), # show all group
                       (r'^$','show_all_group'), # show all group
                       (r'^new$','new'),  # to create a group
                       (r'^create/$','create'),  # post after create
                       (r'^(?P<group_id>\d+)/edit','edit'), # to edit a group
                       #(r'^edit/(?P<group_id>\d+)','edit'), # to edit a group
                       (r'^(?P<group_id>\d+)/update','update'), # post after edit
                       #(r'^update/(?P<group_id>\d+)','update'), # post after edit
                       (r'^(?P<group_id>\d+)/delete','delete'), # to delete a group
                       #(r'^delete/(?P<group_id>\d+)','delete'), # to delete a group
                       (r'^(?P<group_id>\d+)/destroy','destroy'), # to post after delete
                       #(r'^destroy/(?P<group_id>\d+)','destroy'), # to post after delete
                       #(r'^(?P<group_id>\d+)','show'),
                       (r'^(?P<group_id>\d+)','show_group',None),
                       (r'^creategroup$','create_group',None),
                       )