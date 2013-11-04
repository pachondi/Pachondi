# Create your views here.

import logging
from django.contrib.auth.decorators import login_required
from app.users.models import SiteUser
from django.template.context import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy

from app.groups.models import Group, GroupMember
from app.groups.forms import GroupForm, GroupAdminSettingsForm, GroupOwnerSettingsForm, GroupMemberSettingsForm

# get a logging instance
log = logging.getLogger(__name__)

class GroupCreateView(CreateView):
    model = Group
    template_name = 'groups/group_form_create.html' #  else seachers <appname>_form.html
    form_class = GroupOwnerSettingsForm # else shows all Model element
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(GroupCreateView, self).form_valid(form)
    
class GroupUpdateView(UpdateView):
    """
    The main view that controls editing of group information
    based on context and request parameters.
    1. If a regular member or public makes a request
        then a "no access control message" to be displayed
        along with the respective template for member/public
    2. If a moderator/admin (non-owner) makes a request,
        then the user can update the fields based on access control.
        An admin/mod can be let to make almost all changes an owner
        can make except group de-activation and ownership transfer. 
    3. If owner makes the request, he/she can edit anything, including
        deactivating the group and transfer or ownership.
    """
    model = Group
    template_name = 'groups/group_form_update.html' #  else seachers <appname>_form.html
    

    def dispatch(self, request, *args, **kwargs):
        #load the model
        group = Group.objects.get(pk=kwargs['pk']) 
        #and member permissions
        groupmember = GroupMember.objects.get(user=request.user.id,group=group)
         
        if groupmember.is_member_owner:
            return GroupOwnerSettingsUpdateView.as_view()(request, *args, **kwargs)
        elif groupmember.is_member_moderator:
            return GroupAdminSettingsUpdateView.as_view()(request, *args, **kwargs)
        else: #return to the group with a message that you don't have permissions to view
            return GroupDetailView.as_view()(request, *args, **kwargs)

class GroupAdminSettingsUpdateView(UpdateView):
    model = Group
    template_name = 'groups/group_admin_form_update.html'
    form_class = GroupAdminSettingsForm

class GroupOwnerSettingsUpdateView(UpdateView):
    model = Group
    template_name = 'groups/group_owner_form_update.html'
    form_class = GroupOwnerSettingsForm

#there should be a way to merge GroupUpdate and GroupSettingsUpdate into one uber view for the admin
class GroupDetailView(DetailView):
    model = Group
    
    def __init__(self):
        self.__custom_user = None
        self.__custom_permission = None
        
    def dispatch(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['pk'])
        self.__custom_user = request.user.id
        self.__custom_permission = _get_group_membership(group,self.__custom_user) 
        return DetailView.dispatch(self, request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(GroupDetailView,self).get_context_data(**kwargs)
        """ Pass the permission setting""" 
        context['user_access'] = self.__custom_permission
        """ Instantiate member settings form and pass to context """
        if self.__custom_permission not in ["nonmember"]:
            groupmember = GroupMember.objects.get(user=self.__custom_user,group=kwargs['object'])
            groupmembersettingsform = GroupMemberSettingsForm(instance=groupmember)
            context['group_member_settings_form'] = groupmembersettingsform
        
        return context
        
    def get_template_names(self):
        
        if self.__custom_permission == 'nonmember':
            _return_template_name = 'groups/group_detail_nonmember.html'
        elif self.__custom_permission == 'owner':
            _return_template_name = 'groups/group_detail_owner.html'
        
        return _return_template_name
     
def _get_group_membership(group, user):
    
    try:
        _membership = None
        groupmember = GroupMember.objects.get(user=user,group=group)
    except GroupMember.DoesNotExist:    
        _membership = 'nonmember'
    else:
        if groupmember.is_member_owner:
            _membership = 'owner'
        elif groupmember.is_member_moderator:
            _membership = 'admin'
        else: #return to the group with a message that you don't have permissions to view
            _membership = 'member'
     
    return _membership       

class GroupMemberSettingsUpdateView(UpdateView):
    model=GroupMember
    template_name = 'groups/group_member_settings_update.html'
    form_class = GroupMemberSettingsForm
    
    def get_success_url(self):
        return reverse_lazy('group-show', kwargs={'pk':1})
            
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