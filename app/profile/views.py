from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from app.users.models import SiteUser
from app.users.settings.models import UserSettings
from app.profile.forms import UserProfileForm
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from app.users.posts.models import UserPost

@login_required
def profile(request, template_name='profile.html'):
    user = get_object_or_404(SiteUser, id=request.user.id)
    post_signup_redirect = reverse('app.users.settings.views.settings')
            
    try:
        instance = UserSettings.objects.get(pk=user.id)
    except UserSettings.DoesNotExist:
        instance = UserSettings()
        
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():                            
            opts = {}
            opts['user']=user                            
            form.save(**opts)
            return HttpResponseRedirect(post_signup_redirect)            
    else:        
        form = UserProfileForm(instance=instance)
    return render_to_response(template_name, {'form':form,'user': user}, 
                              context_instance=RequestContext(request))
    
@login_required
def view_profile(request, userslug, template_name='view_profile.html', **kwargs):
    user = get_object_or_404(SiteUser, user_slug=userslug)
    current_user=get_object_or_404(SiteUser, id=request.user.id)
    connections = user.relationships.friends()
    posts=UserPost.objects.filter(user__in=list(connections)).order_by('-post_dt')
    add_user=False
    
    if user.id != current_user.id:
        if not current_user.relationships.friends().filter(id=user.id):        
            add_user=True
    return render_to_response(template_name, {'posts':posts,
                                              'connections':connections,
                                              'add_user':add_user,
                                              'user':user }, 
                              context_instance=RequestContext(request))   