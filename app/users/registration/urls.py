from django.conf.urls import patterns, url
from app.users.registration.views import RegistrationView, ConfirmEmailView
from app.users.registration.forms import  RegistrationForm

urlpatterns = patterns('',
                        url('^register', RegistrationView.as_view(form_class=RegistrationForm), name='register_view'),
                        url('^confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', ConfirmEmailView.as_view(), name='signup_confirm'),
                    )