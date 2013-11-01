# Create your views here.

import logging
from django.contrib.auth.decorators import login_required
from app.users.models import SiteUser
from django.template.context import RequestContext
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy

from app.groups.models import Group
from app.groups.forms import GroupForm

# get a logging instance
log = logging.getLogger(__name__)

class GroupCreate(CreateView):
    model = Group
    template_name = 'groups/group_form_create.html' #  else seachers <appname>_form.html
    form_class = GroupForm # else shows all Model element
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(GroupCreate, self).form_valid(form)
    
class GroupUpdate(UpdateView):
    model = Group
    template_name = 'groups/group_form_update.html' #  else seachers <appname>_form.html
    form_class = GroupForm



@login_required
def show_all(request):    
    group_list = Group.objects.filter(_is_active=True)
    user=get_object_or_404(SiteUser, id=request.user.id)
    
    return render_to_response(
               'groups/list.html',                
               {
                'action':'',
                'button':'',
                'group_list':group_list,
                'user':user
                },
                context_instance=RequestContext(request)
           )
    
@login_required
def show_group(request, group_id,message=""):    
    group = Group.objects.get(id=group_id)
    user=get_object_or_404(SiteUser, id=request.user.id)
    
    return render_to_response(
               'groups/group_detail.html',                
               {
                'action':'',
                'button':'',
                'Group':group,
                'user':user,
                'message':message
                },
                context_instance=RequestContext(request)
           )