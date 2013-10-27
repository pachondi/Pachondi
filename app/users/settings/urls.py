from django.conf.urls import patterns, url
from app.users.settings.views import settings

urlpatterns = patterns('',
                        url(r'^settings/$', 
                        settings, 
                        {'template_name': '_settings.html'}),                 
                    )