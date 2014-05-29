from app.goals.views import show_goal
from django.conf.urls import patterns


urlpatterns = patterns('app.goals.views',
   (r'^$', show_goal),
   )



