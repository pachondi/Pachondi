from django.conf.urls import patterns, url
from app.users.authentication.views import LoginView, LogoutView
from app.users.authentication.forms import EmailAuthenticationForm

urlpatterns = patterns('',
                        url('^login$', LoginView.as_view(form_class=EmailAuthenticationForm), name='login_view'),
                        url('^logout$', LogoutView.as_view(), name='logout_view'),                        
                    )