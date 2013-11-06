# Create your views here.
from django.shortcuts import render_to_response, redirect
from app.groups.models import GroupDiscussion, GroupDiscussionMessage


import logging
log = logging.getLogger(__name__)


def index(request, message=""):
    group_disc_msgs_list = GroupDiscussionMessage.objects.all()
    return render_to_response(
        'messages/group_disc_msgs_list.html',
        {'group_disc_msgs_list':group_disc_msgs_list,'message':message}
    )
    
# GET /discussions/new
def new(request):
    return render_to_response(
        'messages/group_disc_msg_form.html',
        {
         'action':'create',
         'button':'Create',
         'action_url':'/group_discussion_messages/create/',
         'belongs_to':request.GET.get('belongs_to')
        }
    )


# POST /discussion
def create(request,reply_for=None):
    """
    reply_for is a message instance. Need to check if this
    is a good idea
    """
    if request.method != "POST":
        return redirect('messages.views.index') #need to point to discussion
    
    if ("belongs_to" not in request.POST or 
        request.POST.get("belongs_to") in ["None",None]):   
            return redirect('messages.views.index')
    
    params = {}
    raw_message = request.POST["raw_message"]
    group_disc = GroupDiscussion.objects.get(id=request.POST.get("belongs_to"))
    params["group_discussion"] = group_disc
    if reply_for:
        params["linked_message"] = reply_for
    else :    
        params["raw_message"] = raw_message
    group_discussion_msg = GroupDiscussionMessage(**params)
    group_discussion_msg.save()
    
    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view, context_referrer_id)
    
    return index(request, "Group Discussion Message Created")


def edit(request,message_id):
    
    if request.method != "POST":
        return redirect('messages.views.new')
    
    if ("belongs_to" not in request.POST or 
        request.POST.get("belongs_to") in ["None",None]):   
            return redirect('messages.views.new')

    # Redirect to delete if requested
    if request.POST["submit_mode"] == "delete":
        return delete(request,message_id)
    
    
    log.debug(request.POST["submit_mode"])
    
    gdm = GroupDiscussionMessage.objects.get(id=message_id)
    
    # Redirect to create if a reply is required 
    if request.POST["submit_mode"] == "reply":
        return create(request,reply_for=gdm)
    
  
    return render_to_response(
               'messages/group_disc_msg_form.html',                
               {
                                    "mode":"edit",
                                    "button":"Update",
                                    "action":"update",
                                    "action_url":"/group_discussion_messages/"+message_id+"/update",
                                    "message_id":message_id,
                                    "raw_message":gdm.raw_message,
                                    "belongs_to":request.POST.get("belongs_to"),
                                    "context_referrer":request.POST.get("context_referrer"),
                                    "context_referrer_id":request.POST.get("context_referrer_id")
                }                   
           )

#PUT /group_discussion_messages/:id/update
def update(request,message_id):
    
    if request.method != "POST":
        return redirect('messages.views.new')
    
    if ("belongs_to" not in request.POST or 
        request.POST.get("belongs_to") in ["None",None]):   
            return redirect('messages.views.index')

    if request.POST["submit_mode"] == "delete":
        return delete(request,message_id)

    gdm = GroupDiscussionMessage.objects.get(id=message_id)
    gdm.raw_message = request.POST["raw_message"]
    gdm.save()

    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view,context_referrer_id)
    
    return index(request,"Group Discussion Message Created")

#DELETE /group_discussion_messages/:id/delete

def delete(request,message_id):
    
    if request.method != "POST":
        return redirect('messages.views.index')
    
    if ("belongs_to" not in request.POST or 
        request.POST.get("belongs_to") in ["None",None]):   
            return redirect('messages.views.index')

    gdm = GroupDiscussionMessage.objects.get(id=message_id)
    gdm.is_active = False
    gdm.save()
    
    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view,context_referrer_id)
    
    return index(request,"Group Discussion Message Deleted")
    

