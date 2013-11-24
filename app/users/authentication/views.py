import urlparse
from django.contrib import auth, messages
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.conf import settings
from app.users.authentication.forms import EmailAuthenticationForm
from django.utils.translation import ugettext as _

class LoginView(FormView):
    """
        in urls.py:
            url(r'^login/$',
                LoginView.as_view(
                    form_class=MyCustomAuthFormClass,
                    success_url='/my/success/url/'),
                name='login'),
    
    
    """
    form_class = EmailAuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = '_login.html'
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if kwargs['template_name'] is not None:
            self.template_name = kwargs['template_name']          
        return super(LoginView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we 
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
        
    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we 
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)
    
    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
    
        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
            # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to
        
    def set_test_cookie(self):
        self.request.session.set_test_cookie()
        
    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False
        
    def get(self, request, *args, **kwargs):
        """
        same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """        
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)
   
class LogoutView(RedirectView):    
    permanent = False
    url='/users/'
    
    def get_redirect_url(self, *args, **kwargs):        
        if self.request.user.is_authenticated():
            messages.add_message(self.request, messages.INFO, _('Logged out.'))
            auth.logout(self.request)        
            
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
