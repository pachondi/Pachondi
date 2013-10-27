# Create your views here.

import logging
from django.contrib.auth.decorators import login_required
from app.users.models import SiteUser
from django.template.context import RequestContext
from app.groups.models import Group
from app.groups.forms import GroupForm
from django.views.generic import DetailView
from django.shortcuts import render_to_response, redirect, get_object_or_404

log = logging.getLogger(__name__)
#from django.http import HttpResponse

# get a logging instance


# GET /groups
@login_required
def index(request, message=""):
    group_list = Group.objects.all()
    return render_to_response(
        'groups/list.html',
        {'group_list':group_list,'message':message}
    )

@login_required
def create_group(request):
    user=get_object_or_404(SiteUser, id=request.user.id)
    
    if request.method == "POST":            
        form = GroupForm(request.POST)
        
        if form.is_valid():                            
            opts = {}
            opts['user']=user
            form.save(**opts)        
            return index(request,"Group Created")
    else:
        form = GroupForm()
        
    return render_to_response('groups/form.html', {'form':form,'user': user}, 
                              context_instance=RequestContext(request)) 

@login_required
def show_all_group(request):    
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
    
# GET /groups/:id
class GroupDetailView(DetailView):
# This is a class based generic view to display one group    
    model = Group # Set the model as Group
    
    """
    Override context to pass additional information to template
    apart from group information. If we don't override, template
    gets on Group object information. Extra contexts passed are
    1. Related discussions on this group.
    """ 
    @login_required
    def get_context_data(self, **kwargs):
        """
        kwargs contains one key 'object' that holds the group
        object. Which means at this level we can get whatever
        we want. Available methods in object:
        ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', 
         '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', 
         '__hash__', '__init__', '__metaclass__', '__module__', '__ne__', 
         '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
         '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', 
         '_base_manager', '_default_manager', '_deferred', '_get_FIELD_display', 
         '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', 
         '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', 
         '_perform_unique_checks', '_set_pk_val', '_state', 'clean', 'clean_fields', 
         'date_error_message', 'delete', 'description', 'full_clean', 
         'get_detail_fields', 'groupdiscussion_set',  'id', 'is_active', 'name', 
         'objects', 'pk', 'prepare_database_save', 'save', 'save_base', 
         'serializable_value', 'unique_error_message', 'validate_unique'
         ]
         
         self has
             class django.views.generic.detail.SingleObjectTemplateResponseMixin
                 'template_name_field', 'template_name_suffix', 'get_template_names'()
             class django.views.generic.base.TemplateResponseMixin
                 'template_name','response_class','render_to_response','get_template_names'()
             class django.views.generic.detail.SingleObjectMixin
                  'model','queryset', 'slug_field', 'slug_url_kwarg', 'pk_url_kwarg','context_object_name'
                  'get_object', 'get_queryset', 'get_slug_field','get_context_object_name','get_context_data',
             class django.views.generic.base.View
                   'http_method_names','as_view','dispatch','http_method_not_allowed',
                     
        ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', 
        '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', 
        '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_
        _weakref__', 'args',  'get', 'head','kwargs', , 'object', ,  , 'request',
        ]
        """
        context = super(GroupDetailView,self).get_context_data(**kwargs)
        group_form = GroupForm(instance=kwargs["object"])
        context["display_context"] = {
                                    "mode":"show",
                                    "button":"Edit",
                                    "action":"edit",
                                    "group_form": group_form
                                   } 
        """
        Now this is one way to do it. But we don't want any 
        processing logic in the views. So get_group_discussions
        in the Group Model will handle data processing.
        # context["group_discussions_list"] =  GroupDiscussion.objects.filter(group__id__exact = "1")
        """
        
        return context
    
# GET /groups/:id
@login_required
def show(request, group_id, message=""):
    group = Group.objects.get(id=group_id)
    user=get_object_or_404(SiteUser, id=request.user.id)
    
    return render_to_response(
               'groups/form.html',                
               {
                'action':'',
                'button':'',
                'Group':group,
                'user':user,
                'message':message
                }                   
           )

# GET /groups/new
@login_required
def new(request):
    return render_to_response(
        'groups/form.html',
        {
         'action':'create',
         'button':'Create'
        }
    )

# POST /groups
@login_required
def create(request):
    user=get_object_or_404(SiteUser, id=request.user.id)
    
    if request.method == "POST":            
        form = GroupForm(request.POST)
        
        if form.is_valid():                            
            opts = {}
            opts['created_by']=user
            form.save(**opts)        
            return index(request,"Group Created")
    else:
        form = GroupForm()
        
    return render_to_response('groups/form.html', {'form':form,'user': user}, 
                              context_instance=RequestContext(request)) 
    
    """
    group_name = request.POST["name"]
    group_description = request.POST["description"]
    group_type = request.POST["type"]
    group_website = request.POST["group_website"]
    group = Group(
                 name = group_name,
                 description = group_description,
                 type=group_type,
                 website=group_website
            )
    group.save()
    return index(request,"Group Created")"""

#GET /groups/:id/edit
@login_required
def edit(request,group_id):
    
       
    group = Group.objects.get(id=group_id)
    group_form = GroupForm(instance=group)
    return render_to_response(
               'groups/group_detail.html',                
               {
                'display_context':{
                                    "mode":"edit",
                                    "button":"Update",
                                    "action":"update",
                                    "group_form":group_form
                                   },
                'object':group
                }                   
           )

#PUT /groups/:id
@login_required
def update(request,group_id):
    
    if request.method != "POST":
        return index(request,message="The requested path is not supported. Please browse recommended groups.")  

    group = Group.objects.get(id=group_id)
    group.name = request.POST["group_name"]
    group.description = request.POST["group_description"]
    group.save()
    '''
    Three ways to redirect. 
    1. Pass the absolute url
    2. Pass the view name and key for a reverse lookup, if enabled in urls.py
    3. redirect to the object, IIF get_absolute_url is defined for the object
    '''
    return redirect(group)
    # return redirect("show-group",group_id) #
    # return show(request,group_id,message="Group " + group.name + " Updated.")   
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)

#GET /groups/:id/delete
@login_required
def delete(request,group_id):
    group = Group.objects.get(id=group_id)
    return render_to_response(
               'groups/form.html',                
               {
                'action':group_id+'/destroy',
                'button':'Delete',
                'Group':group
                }                   
           )

#DELETE /groups/:id
@login_required
def destroy(request,group_id):

    if request.method != "POST":
        return redirect('groups.views.index')

    group_name = request.POST["name"]
    Group.objects.get(id=group_id).delete()
    return index(request,message="Group " + group_name + " Deleted.")

#def groups_home(request):
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)
    
"""
# GET /groups
  def index
    @groups = Group.all
  end
  
  
  # GET /groups/:id
  def show
    #@groups = Group.where("user_id = ?",current_user.id)
    @group = Group.find(params[:id])
  end

  # GET /groups/new
  def new
    @group = Group.new
  end
  
  # POST /groups
  def create
    params[:group].merge!("user_id" => @current_user.id)
    @group = Group.new(params[:group])
    if @group.save
      flash[:notice] = "Group created! #{params} #{params[:group]}"
      redirect_back_or_default groups_path
    else
      render :action => :new
    end
  end
  
  #GET /groups/:id/edit
  def edit
    @group = Group.find(params[:id])
  end  
  
  #PUT /groups/:id
  def update
    @group = Group.find(params[:id])
    
    if @group.update_attributes(params[:group])
      flash[:notice] = "Group was successfully updated #{params}"
      respond_with @group, :location => groups_path
    end
    # rails 2 way
    #respond_to do |format|
      #if @group.update_attributes(params[:group])
        #format.html { redirect_to @group, notice:'Group was successfully updated'}
      #else
        #format.html { render action:"edit", notice:'Group was unsuccessfully updated'}
      #end
    #end 
  
  end
  
  #DELETE /groups/:id
  def destroy
    #Can only deactivate if the group was created by the owner
    #should only deactivate and not delete the group.  
    Group.find(params[:id]).destroy
    flash[:notice] = "Group Deleted!"
    redirect_back_or_default groups_path
  end
  """