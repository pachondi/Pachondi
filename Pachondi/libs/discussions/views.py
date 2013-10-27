# Create your views here.
from app.groups.models import Group, GroupDiscussion
from django.shortcuts import render_to_response, redirect
# from django.template import RequestContext

# Create your views here.

# GET /discussions
def index(request, message=""):
    group_discussion_list = GroupDiscussion.objects.all()
    return render_to_response(
        'discussions/list.html'
        ,{'group_discussion_list':group_discussion_list,'message':message}
        #,context_instance=RequestContext(request) # no need to do this is using Generic View
        # http://stackoverflow.com/questions/10355194/how-to-serve-static-files-for-local-development-in-django-1-4
    )


# GET /discussions/new
def new(request):
    return render_to_response(
        'discussions/group_discussion_form.html',
        {
         'action':'create',
         'button':'Create',
         'belongs_to':request.GET.get('belongs_to'),
         'action_url':'/group_discussions/create/'
        }
    )


# POST /discussion
def create(request):
    if request.method != "POST":
        return redirect('discussions.views.new')
    
    if not request.POST.get("belongs_to"):
        return redirect('discussions.views.new')

    params = {}
    name = request.POST["name"]
    group = Group.objects.get(id=request.POST.get("belongs_to"))
    params["name"] = name
    params["group"] = group
    group_discussion = GroupDiscussion(**params)     
    group_discussion.save()
    
    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view,context_referrer_id)
    
    return index(request,"Group Discussion Created")

def edit(request,discussion_id):
    
    gd = GroupDiscussion.objects.get(id=discussion_id)
    
    return render_to_response(
               'discussions/group_discussion_form.html',                
               {
                                    "mode":"edit",
                                    "button":"Update",
                                    "action":"update",
                                    "action_url":"/group_discussions/"+discussion_id+"/update",
                                    "discussion_id":discussion_id,
                                    "discussion_name":gd.name,
                                    "belongs_to":request.POST.get("belongs_to"),
                                    "context_referrer":request.POST.get("context_referrer"),
                                    "context_referrer_id":request.POST.get("context_referrer_id")
                }                   
           )

#PUT /groups/:id
def update(request,discussion_id):
    
    gd = GroupDiscussion.objects.get(id=discussion_id)
    gd.name = request.POST["name"]
    gd.save()

    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view,context_referrer_id)
    
    return index(request,"Group Discussion Message Created")

def show(request,pk):
    groupdiscussion = GroupDiscussion.objects.get(id=pk)
    return render_to_response(
        'discussions/group_discussion_detail.html',
        {
         'gd':groupdiscussion,
         'link_pk':pk
        }
    )
