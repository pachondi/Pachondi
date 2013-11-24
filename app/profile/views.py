from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from app.users.models import SiteUser
from app.profile.forms import UserProfileForm, UserProfileSkillForm, UserProfileEducationForm,\
    UserProfileCompanyForm
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from app.users.posts.models import UserPost
from app.profile.models import UserProfile
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

@login_required
def profile(request, template_name='profile.html'):
    user = get_object_or_404(SiteUser, id=request.user.id)
    post_signup_redirect = reverse('app.users.settings.views.settings')
            
    try:
        instance = UserProfile.objects.get(pk=user.id)
    except UserProfile.DoesNotExist:
        instance = UserProfile()
        
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
    user_profile = user.userprofiles.get_default_profile()       
    user_profile_company=user_profile.companies.get_companies()
    user_profile_education=user_profile.schools.get_education()
    user_profile_skills=user_profile.skills.get_skills()   
    add_user=False
    
    if user.id != request.user.id:
        if not request.user.relationships.friends().filter(id=user.id):        
            add_user=True
            
    return render_to_response(template_name,{'profile' : user_profile,
                                             'companies': user_profile_company,
                                             'education': user_profile_education,
                                             'skills':user_profile_skills,
                                             'add_user':add_user
                                             },context_instance=RequestContext(request))  
    
    
@login_required
def my_profile(request, *args, **kwargs):    
    has_user_profile = request.user.userprofiles.has_default_profile()
        
    if(has_user_profile == False):
        return redirect('/profile/step-by-step')
    
    user_profile = request.user.userprofiles.get_default_profile()       
    user_profile_company=user_profile.companies.get_companies()
    user_profile_education=user_profile.schools.get_education()
    user_profile_skills=user_profile.skills.get_skills()
    return render_to_response(kwargs['template_name'],{'profile' : user_profile,
                                             'companies': user_profile_company,
                                             'education': user_profile_education,
                                             'skills':user_profile_skills 
                                             },context_instance=RequestContext(request))

                              
FORMS = [("basic", UserProfileForm),
         ("company", UserProfileCompanyForm),
         ("education", UserProfileEducationForm),
         ("skills", UserProfileSkillForm)]

TEMPLATES = {"basic": "wizard/_current.html",
             "company": "wizard/_company.html",
             "education": "wizard/_education.html",
             "skills": "wizard/_skills.html"}

def currently_studying(wizard):
    """Return true if user opts to pay by credit card"""
    # Get cleaned data from payment step
    cleaned_data = wizard.get_cleaned_data_for_step('basic') or {'current_status': 'none'}
    # Return true if the user selected student
    return cleaned_data['current_status'] == 'S'

def currently_working(wizard):
    """Return true if user opts to pay by credit card"""
    # Get cleaned data from payment step
    cleaned_data = wizard.get_cleaned_data_for_step('basic') or {'current_status': 'none'}
    # Return true if the user selected student
    return cleaned_data['current_status'] == 'E' 


class ProfileWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    #template_name='wizard.html'
    
    def dispatch(self, request, *args, **kwargs):
        has_user_profile = request.user.userprofiles.has_default_profile()
        
        if(has_user_profile):
            return redirect('/profile/myprofile')
        
        return super(ProfileWizard, self).dispatch(request, *args, **kwargs)
    
    def done(self, form_list, **kwargs):
        try:
            for form in form_list:
                form.save(self.request)
        except:            
            raise
        
        return HttpResponseRedirect('/profile/myprofile/')
        
    def get_form(self, step=None, data=None, files=None):
        form = super(ProfileWizard, self).get_form(step, data, files)
        
        # determine the step if not given
        if step is None:
            step = self.steps.current
    
        form.user = self.request.user
        return form

    def process_step(self, form):
        form.user = self.request.user        
        return self.get_form_step_data(form)
