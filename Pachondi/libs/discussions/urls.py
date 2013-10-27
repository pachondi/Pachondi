from django.conf.urls import patterns

urlpatterns = patterns('Pachondi.libs.discussions.views',
                        (r'$','index'),
                        (r'new$','new',None,'new-group-discussion'),
                        (r'create/$','create'),
                        (r'(?P<discussion_id>\d+)/edit','edit',None,'edit-group-discussion'),
                        (r'(?P<discussion_id>\d+)/update','update',None,'update-group-discussion'),
)