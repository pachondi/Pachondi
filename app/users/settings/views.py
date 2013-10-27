from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from app.users.models import SiteUser
from app.users.settings.forms import UserSettingsForm
from app.users.settings.models import UserSettings
from django.template.context import RequestContext
from django.core.urlresolvers import reverse

@login_required    
def settings(request, template_name='_settings.html',settings_form=UserSettingsForm):
    user = get_object_or_404(SiteUser, id=request.user.id)        
    try:
        instance = UserSettings.objects.get(pk=user.id)
    except UserSettings.DoesNotExist:
        instance = UserSettings()
        
    if request.method == "POST":        
        form = settings_form(request.POST, instance=instance)
        if form.is_valid():
            opts = {}
            opts['user']=user
            form.save(**opts)            
    else:
        form = settings_form(instance=instance)
        
    return render_to_response(template_name, {'user': user, 'form':form}, 
                              context_instance=RequestContext(request))
