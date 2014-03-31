from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from app.users.models import SiteUser
from app.users.registration.forms import RegistrationForm
from app.users.authentication.forms import EmailAuthenticationForm
from app.users.posts.models import UserPost

@csrf_protect
def index(request, template_name = 'index.html', 
          login_form = EmailAuthenticationForm,
          signup_form = RegistrationForm,
          **kwargs):
    if request.user.is_authenticated():
        return redirect('/users/home', **kwargs)
    
    return render_to_response(template_name, 
                               {'login_form' : login_form, 'signup_form' : signup_form},
                        context_instance=RequestContext(request))

@login_required

def home(request, template_name):
    user = get_object_or_404(SiteUser, id=request.user.id)
    connections = user.relationships.friends()
    suggested_connections = user.relationships.suggestions(connections) 
    #suggested_connections = get_connection_suggestion(user)    
    
    #connections = user.connections.all()
    connection_requests=user.relationships.received_requests()
    #try:        
        #connection_requests=ConnectionRequest.objects.filter(to_user=user,status='R')
    #except ObjectDoesNotExist:
    #   print("No connection request for user.")
        
    posts=UserPost.objects.filter(user__in=list(connections)).order_by('-post_dt')
    return render_to_response(template_name, {'posts':posts,
                                              'connections':connections,
                                              'connection_requests':connection_requests,
                                              'suggested_connections':suggested_connections,
                                              'user':user }, 
                              context_instance=RequestContext(request))
    