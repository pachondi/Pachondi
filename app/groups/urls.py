from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required
from app.groups.views import GroupCreateView, GroupUpdateView, GroupDetailView, GroupMemberSettingsUpdateView

#http://www.wellfireinteractive.com/blog/fast-and-beautiful-urls-with-django/
urlpatterns = patterns('app.groups.views',
                       #(r'^$','show_all',None,'show-group-all'), # show all group
                       (r'^create$',login_required(GroupCreateView.as_view()),None,'group-create'),
                       (r'^(?P<pk>\d+)/edit$',login_required(GroupUpdateView.as_view()),None,'group-update'),
                       (r'^(?P<pk>\d+)$',GroupDetailView.as_view(),None,'group-show'),
                       (r'^member/(?P<pk>\d+)/edit$',login_required(GroupMemberSettingsUpdateView.as_view()),None,'group-member-settings-update'),
                       )