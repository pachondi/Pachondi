from django.conf.urls import patterns, url
from app.users.views import index, home
from app.users.authentication.views import LoginView, LogoutView
from app.users.authentication.forms import EmailAuthenticationForm
from app.users.registration.views import RegistrationView, ConfirmEmailView
from app.users.registration.forms import RegistrationForm
from app.users.settings.views import settings
from app.users.posts.views import add_post, delete_post, post_comment, delete_comment
#from users.api import SiteUserResource

#siteuser_resource = SiteUserResource()
"""
(r'^login/$', 
 custom_login, 
 {'template_name': 'users/login.html'}),

(r'^logout/$', 
 'custom_logout', 
 {'template_name': 'users/logged_out.html'}),
 """
urlpatterns = patterns('app.users.authentication',                       
                        url(r'^login$', 
                            LoginView.as_view(form_class=EmailAuthenticationForm), 
                            {'template_name': 'users/login.html'},
                            name='login_view'),
                       
                        url('^logout$', 
                            LogoutView.as_view(), 
                            name='logout_view'),    
)
urlpatterns += patterns('app.users.registration.views',
                        url('^register', 
                            RegistrationView.as_view(form_class=RegistrationForm),
                            {'template_name': 'users/register.html'}, 
                            name='register_view'),
                        
                        url('^register/action', 
                            'perform_action',
                            {'template_name': 'step1.html'}, 
                            name='register_action'),
                        
                        url('^confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 
                            ConfirmEmailView.as_view(), 
                            name='signup_confirm'),
)
urlpatterns += patterns('app.users.settings',
                        url(r'^settings$', 
                        settings, 
                        {'template_name': 'users/settings.html'}),       
)

urlpatterns += patterns('app.users.posts',
                        (r'^post/(?P<user_id>\d+)/add$', add_post),
                       
                       (r'^post/(?P<post_id>\d+)/remove$', delete_post),
                       
                       (r'^post/(?P<post_id>\d+)/comment/add$', post_comment),
                       
                       (r'^post/comment/(?P<comment_id>\d+)/remove$', delete_comment),
)

urlpatterns += patterns('app.users.views',
                       (r'^index$', index,{'template_name': 'users/index.html'}),
                       
                       (r'^home$', home,{'template_name': 'users/home.html'}),             
                       
                       #(r'^api/', include(siteuser_resource.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
                (r'^password_change/$', 
                        'password_change', 
                        {'template_name': 'users/password_change_form.html'}),

                       (r'^password_change/done/$', 
                        'password_change_done', 
                        {'template_name': 'users/password_change_done.html'}),

                       (r'^password_reset/$', 
                        'password_reset', 
                        {'template_name': 'users/password_reset_form.html',
                         'email_template_name': 'users/password_reset_email.html'}),

                       (r'^password_reset/done/$', 
                        'password_reset_done', 
                        {'template_name': 'users/password_reset_done.html'}),

                       (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
                        'password_reset_confirm', 
                        {'template_name': 'users/password_reset_confirm.html'}),

                       (r'^reset/done/$', 
                        'password_reset_complete', 
                        {'template_name': 'users/password_reset_complete.html'}),                
                )