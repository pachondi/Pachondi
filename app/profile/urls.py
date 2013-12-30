from django.conf.urls import patterns, url
from app.profile.views import profile, view_profile, my_profile, profile_basic,\
    profile_company, profile_skills, profile_education


urlpatterns = patterns('app.profile',
                       (r'^$', 
                        profile,  
                        {'template_name': 'profile.html'}),                       
                       
                       (r'^(?P<userslug>([a-zA-Z]*).([a-zA-Z]*).\d+-\d+-\d+)$', view_profile),
                        url(r'^basic/$',profile_basic, name='profile_basic'),
                        url(r'^basic/(?P<profile_id>([0-9]*))$',profile_basic, name='profile_basic'),
                        url(r'^(?P<profile_id>([0-9]*))/company/$',profile_company, name='profile_company'),
                        url(r'^(?P<profile_id>([0-9]*))/company/(?P<id>\d+)$',profile_company, name='profile_company'),
                        url(r'^(?P<profile_id>([0-9]*))/education/$',profile_education, name='profile_education'),
                        url(r'^(?P<profile_id>([0-9]*))/education/(?P<id>\d+)$',profile_education, name='profile_education'),
                        url(r'^(?P<profile_id>([0-9]*))/skills/$',profile_skills, name='profile_skills'),
                        url(r'^(?P<profile_id>([0-9]*))/skills/(?P<id>\d+)$',profile_skills, name='profile_skills'),
                       url(r'^myprofile/(?P<profile_id>([0-9]*))$', my_profile, {'template_name':'my_profile.html'}, name='my_profile'),
                       (r'^myprofile/(?P<type>([a-zA-Z]*))/add$', my_profile, {'template_name':'my_profile.html'}),
                       (r'^myprofile/(?P<type>([a-zA-Z]*))/(?P<id>\d+)/edit$', my_profile, {'template_name':'my_profile.html'})
                        )