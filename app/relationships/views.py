from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson as json
from django.utils.http import urlquote
from app.relationships.decorators import require_user
from app.relationships.models import RelationshipStatus
from django.views.generic.list import ListView
from app.users.models import SiteUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

class RelationshipListView(ListView):
    model = SiteUser
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if kwargs['template_name'] is not None:
            self.template_name = kwargs['template_name']          
        return super(RelationshipListView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(RelationshipListView, self).get_context_data(**kwargs)        
        return context
    
    def get_queryset(self):
        
        status_slug = self.kwargs['status_slug']
        
        if not status_slug:
            status = RelationshipStatus.objects.following()
            status_slug = status.from_slug
        else:
        # get the relationship status object we're talking about
            status = get_relationship_status_or_404(status_slug)   
            
        # get a queryset of users described by this relationship
        if status.from_slug == status_slug:
            qs = self.request.user.relationships.get_relationships(status=status)
        elif status.to_slug == status_slug:
            qs = self.request.user.relationships.get_related_to(status=status)
        else:
            qs = self.request.user.relationships.get_relationships(status=status, symmetrical=True)
        
        return qs
        
    def render_to_response(self, context, **kwargs):
        return super(RelationshipListView, self).render_to_response(context, **kwargs)



@login_required
def relationship_redirect(request):
    return HttpResponseRedirect(reverse('relationship_list', args=[request.user.email]))

def _relationship_list(request, queryset, template_name=None, *args, **kwargs):
    return ListView(
        request=request,
        queryset=queryset,
        paginate_by=20,
        page=int(request.GET.get('page', 0)),
        template_object_name='relationship',
        template_name=template_name,
        *args,
        **kwargs
    )

def get_relationship_status_or_404(status_slug):
    try:
        return RelationshipStatus.objects.by_slug(status_slug)
    except RelationshipStatus.DoesNotExist:
        raise Http404

        
@login_required
@require_user
def relationship_list(request, user, status_slug=None,
                      template_name='relationships/relationship_list.html'):
    if not status_slug:
        status = RelationshipStatus.objects.following()
        status_slug = status.from_slug
    else:
        # get the relationship status object we're talking about
        status = get_relationship_status_or_404(status_slug)
    
    # do some basic authentication
    if status.login_required and not request.user.is_authenticated():
        path = urlquote(request.get_full_path())
        tup = settings.LOGIN_URL, 'next', path
        return HttpResponseRedirect('%s?%s=%s' % tup)
    
    if status.private and not request.user == user:
        raise Http404
    
    # get a queryset of users described by this relationship
    if status.from_slug == status_slug:
        qs = user.relationships.get_relationships(status=status)
    elif status.to_slug == status_slug:
        qs = user.relationships.get_related_to(status=status)
    else:
        qs = user.relationships.get_relationships(status=status, symmetrical=True)
    
    ec = dict(
        from_user=user,
        status=status,
        status_slug=status_slug,
    )
    
    return _relationship_list(request, qs, template_name, extra_context=ec)

@login_required
@require_user
def relationship_handler(request, user, status_slug, add=True,
                         template_name='relationships/confirm.html',
                         success_template_name='relationships/success.html'):
    
    status = get_relationship_status_or_404(status_slug)
    is_symm = status_slug == status.symmetrical_slug
    
    if request.method == 'POST':
        if add:
            request.user.relationships.add(user, status, is_symm)
        else:
            request.user.relationships.remove(user, status, is_symm)
        
        if request.is_ajax():
            response = {'result': '1'}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET['next'])
        
        template_name = success_template_name
    
    return render_to_response(template_name, 
        {'to_user': user, 'status': status, 'add': add},
        context_instance=RequestContext(request))


@login_required
def request_connect(request, uid, **kwargs):
    to_user = SiteUser.objects.get(pk=uid)
    status = RelationshipStatus.objects.requesting()
    request.user.relationships.add(to_user, status)
    
    return redirect('/users/home', **kwargs)

@login_required
def delete_request_connect(request, uid, **kwargs):
    to_user = SiteUser.objects.get(pk=uid)
    request.user.connectionrequests.delete_request(to_user)
    
    return redirect('/users/home', **kwargs)

@login_required
def accept_connect(request, uid, **kwargs):
    from_user = SiteUser.objects.get(pk=uid)
    status = RelationshipStatus.objects.requesting()
    request.user.relationships.accept(from_user, status, True)
    
    return redirect('/users/home', **kwargs)

@login_required
def decline_connect(request, uid, **kwargs):
    from_user = SiteUser.objects.get(pk=uid)
    request.user.connectionrequests.accept_request(from_user)
    
    return redirect('/users/home', **kwargs)
