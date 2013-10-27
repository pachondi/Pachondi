from django.conf.urls import patterns
from app.profile.views import profile, view_profile

urlpatterns = patterns('app.profile',
                       (r'^$', 
                        profile, 
                        {'template_name': 'profile.html'}),                       
                       
                       (r'^(?P<userslug>([a-zA-Z]*).([a-zA-Z]*).\d+-\d+-\d+)$', view_profile),
                       )