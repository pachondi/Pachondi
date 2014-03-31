from django.contrib.auth import login, REDIRECT_FIELD_NAME, authenticate
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView
from app.users.registration.forms import RegistrationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template.context import RequestContext
from django.utils.http import base36_to_int
from app.users.models import SiteUser
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import ugettext as _

class RegistrationView(FormView):
    form_class = RegistrationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = '_register.html'
    token_generator=default_token_generator
    email_template_name='signup_email.html'
    post_signup_redirect=None
        
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if kwargs['template_name'] is not None:
            self.template_name = kwargs['template_name'] 
        return super(RegistrationView, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """
        same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        #self.set_test_cookie()
        form = RegistrationForm()
        return render_to_response(self.template_name, {'form': form,}, 
                                context_instance=RequestContext(request))
        #return super(RegistrationView, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):        
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        
        opts = {}
        opts['use_https'] = self.request.is_secure()
        opts['token_generator'] = self.token_generator
        opts['email_template_name'] = self.email_template_name
        #if not Site._meta.installed:
        opts['domain_override'] = get_current_site(self.request).domain
        
        """
        The user has provided valid information (this was checked in RegistrationForm.is_valid()). So now we 
        can create the user and log him in.
        """                     
        user = form.save(**opts)
        if user is not None:           
            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                if user.is_active:
                    messages.add_message(self.request, messages.INFO, _('User registered, Kindly verify your email for full access.'))
                    login(self.request, user)
                    # Redirect to a success page.
                    #else:
                    # Return a 'disabled account' error message                
                    return HttpResponseRedirect('/users/registration/step1')                
            else:
                messages.add_message(self.request, messages.INFO, _('Thanks for registering with us, kindly login.'))
                return HttpResponseRedirect('/users/login')
        else:
            messages.add_message(self.request, messages.ERROR, _('Problem registering user.'))
            return HttpResponseRedirect('/users/register')
            

        
        return super(RegistrationView, self).form_valid(form)
        
    def form_invalid(self, form):
        """
        The user has provided invalid information (this was checked in RegistrationForm.is_valid()). So now we 
        set the test cookie again and re-render the form with errors.
        """
        #self.set_test_cookie()
        return super(RegistrationView, self).form_invalid(form)
    
class ConfirmEmailView(RedirectView):
    permanent = False
    url='/users'
    
    def get_redirect_url(self, uidb36=None, token=None,
                   token_generator=default_token_generator, *args, **kwargs):        
        try:
            uid_int = base36_to_int(uidb36)
        except ValueError:
            raise Http404
    
        user = get_object_or_404(SiteUser, id=uid_int)
        context_instance = RequestContext(self.request)
    
        if token_generator.check_token(user, token):
            context_instance['validlink'] = True
            user.is_active = True
            user.is_verified = True
            user.save()
        else:
            context_instance['validlink'] = False
            
        return super(ConfirmEmailView, self).get_redirect_url(*args, **kwargs)

def perform_action(request, template_name):    
    return render_to_response(template_name, context_instance=RequestContext(request))