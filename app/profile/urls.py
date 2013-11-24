from django.conf.urls import patterns
from app.profile.views import profile, view_profile, ProfileWizard, FORMS,\
     currently_studying, currently_working, my_profile

urlpatterns = patterns('app.profile',
                       (r'^$', 
                        profile, 
                        {'template_name': 'profile.html'}),                       
                       
                       (r'^(?P<userslug>([a-zA-Z]*).([a-zA-Z]*).\d+-\d+-\d+)$', view_profile),
                        (r'^step-by-step/$', 
                            ProfileWizard.as_view(FORMS, 
                                                condition_dict={'company': currently_working})),
                       (r'^myprofile/$', my_profile, {'template_name':'my_profile.html'}),
                       (r'^myprofile/(?P<type>([a-zA-Z]*))/add$', my_profile, {'template_name':'my_profile.html'}),
                       (r'^myprofile/(?P<type>([a-zA-Z]*))/(?P<id>\d+)/edit$', my_profile, {'template_name':'my_profile.html'})
                        )