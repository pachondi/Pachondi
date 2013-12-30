from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from app.users.models import SiteUser
from app.profile.forms import UserProfileForm, UserProfileSkillForm, UserProfileEducationForm,\
    UserProfileCompanyForm
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from app.users.posts.models import UserPost
from app.profile.models import UserProfile, UserProfileCompany,\
    UserProfileEducation, UserProfileSkills
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from Pachondi.settings import MEDIA_ROOT

@login_required
def profile(request, template_name='profile.html'):
    profiles = request.user.userprofiles.get_masked_profiles()
    default=request.user.userprofiles.get_default_profile()
    return render_to_response(template_name, {'profiles':profiles,'default_profile':default,'user': request.user}, 
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
def my_profile(request, profile_id, *args, **kwargs):    
    user_profile = request.user.userprofiles.get_profile(profile_id)
        
    if(user_profile is None):
        return redirect(reverse('profile_basic'))
               
    user_profile_company=user_profile.companies.get_companies()
    user_profile_education=user_profile.schools.get_education()
    user_profile_skills=user_profile.skills.get_skills()
    return render_to_response(kwargs['template_name'],{'profile' : user_profile,
                                             'companies': user_profile_company,
                                             'education': user_profile_education,
                                             'skills':user_profile_skills,
                                             'profile_id':profile_id
                                             },context_instance=RequestContext(request))

def save_file(file, path=''):
    ''' Little helper to save a file
    '''
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
            
@login_required
def profile_basic(request, profile_id=0, template_name='_current.html'):        
    try:
        instance = UserProfile.objects.get(pk=profile_id)
    except UserProfile.DoesNotExist:
        instance = UserProfile()
        
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():                            
            opts = {}
            opts['user']=request.user
            opts['instance']=instance
            if(request.user.userprofiles.has_default_profile() == False):
                opts['is_default']=True
            else:
                opts['is_default']=None
            
            form.save(**opts)
            save_file(request.FILES['profile_photo'])
            
            post_action_redirect = reverse('profile_company', kwargs={'profile_id':instance.id})
            
            if instance.current_status == 'S':
                post_action_redirect = reverse('profile_education', kwargs={'profile_id':instance.id})
            return HttpResponseRedirect(post_action_redirect)            
    else:
        form = UserProfileForm(instance=instance)
    return render_to_response(template_name, {'form':form,'user': request.user,'profile_id':profile_id}, 
                              context_instance=RequestContext(request))
    
@login_required
def profile_company(request, profile_id, id=0, template_name='_company.html'):    
    post_action_redirect = reverse('profile_education', kwargs={'profile_id': profile_id})
                    
    try:
        user_profile = UserProfile.objects.get(pk=profile_id)
        user_profile_companies=user_profile.companies.get_companies()
        instance = UserProfileCompany.objects.get(pk=id)
    except UserProfileCompany.DoesNotExist:
        instance = UserProfileCompany()
        
    if request.method == "POST":
        form = UserProfileCompanyForm(request.POST)
        if form.is_valid():                            
            opts = {}
            opts['user']=request.user
            opts['instance']=instance
            opts['profile']=user_profile            
            form.save(**opts)            
            return HttpResponseRedirect(post_action_redirect)            
    else:
        form = UserProfileCompanyForm(instance=instance)
    return render_to_response(template_name, {'profile_id': profile_id,'form':form,'user': request.user, 'companies': user_profile_companies}, 
                              context_instance=RequestContext(request))
    
@login_required
def profile_education(request, profile_id, id=0, template_name='_education.html'):    
    post_action_redirect = reverse('profile_skills', kwargs={'profile_id': profile_id})
            
    try:
        user_profile = UserProfile.objects.get(pk=profile_id)
        instance = UserProfileEducation.objects.get(pk=id)
    except UserProfileEducation.DoesNotExist:
        instance = UserProfileEducation()
        
    if request.method == "POST":
        form = UserProfileEducationForm(request.POST)
        if form.is_valid():                            
            opts = {}
            opts['user']=request.user
            opts['instance']=instance
            opts['profile']=user_profile
            form.save(**opts)
            return HttpResponseRedirect(post_action_redirect)            
    else:
        form = UserProfileEducationForm(instance=instance)
    return render_to_response(template_name, {'profile_id': profile_id,'form':form,'user': request.user}, 
                              context_instance=RequestContext(request))
    
@login_required
def profile_skills(request, profile_id, id=0, template_name='_skills.html'):    
    post_action_redirect = reverse('my_profile')
            
    try:
        user_profile = UserProfile.objects.get(pk=profile_id)
        instance = UserProfileSkills.objects.get(pk=id)
    except UserProfileSkills.DoesNotExist:
        instance = UserProfileSkills()
        
    if request.method == "POST":
        form = UserProfileSkillForm(request.POST, request.FILES)
        if form.is_valid():                            
            opts = {}
            opts['user']=request.user
            opts['instance']=instance
            opts['profile']=user_profile
            form.save(**opts)
            return HttpResponseRedirect(post_action_redirect)            
    else:
        form = UserProfileSkillForm(instance=instance)
    return render_to_response(template_name, {'profile_id': profile_id,'form':form,'user': request.user}, 
                              context_instance=RequestContext(request))    
    
FORMS = [("basic", UserProfileForm),
         ("company", UserProfileCompanyForm),
         ("education", UserProfileEducationForm),
         ("skills", UserProfileSkillForm)]

TEMPLATES = {"basic": "wizard/_current.html",
             "company": "wizard/_company.html",
             "education": "wizard/_education.html",
             "skills": "wizard/_skills.html"}


def currently_working(wizard):
    """Return true if user selects employee as current status"""
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
                 
                if form.is_multipart():
                    self.save_file(self.request.FILES['image'])
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
        return super(ProfileWizard, self).process_step(form)

    def save_file(self, file_data, path=''):
        ''' Little helper to save a file
        '''
        filename = file_data._get_name()
        fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
        for chunk in file.chunks():
            fd.write(chunk)
        fd.close()