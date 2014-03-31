from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile
from django.contrib import messages

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
UNVERIFIED_EXEMPT_URLS= [compile(settings.LOGIN_UNVERIFIED_REDIRECT_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
if hasattr(settings, 'LOGIN_UNVERIFIED_EXEMPT_URL'):
    UNVERIFIED_EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_UNVERIFIED_EXEMPT_URL]
    
class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
        requires authentication middleware to be installed. Edit your\
        MIDDLEWARE_CLASSES setting to insert\
        'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
        work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
        'django.core.context_processors.auth'."
        path = request.path_info.lstrip('/')
        path = path.rstrip('/')
        
        if not request.user.is_authenticated():            
            if not any(m.match(path) for m in EXEMPT_URLS):
                if path:
                    return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + path)
                else:
                    return HttpResponseRedirect(settings.LOGIN_URL)
            
        else:
            if not request.user.is_verified:
                if not any(m.match(path) for m in UNVERIFIED_EXEMPT_URLS):
                    messages.add_message(request, messages.WARNING, 'Email address not verified kindly verify to start using our services.', 'warning')
                    messages.add_message(request, messages.INFO, 'Meanwhile, let us know more about you so that we can get into action.', 'info')
                    return HttpResponseRedirect(settings.LOGIN_UNVERIFIED_REDIRECT_URL)
                