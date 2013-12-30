from django.forms.models import ModelForm
from app.profile.models import UserProfile, UserProfileCompany,\
    UserProfileEducation, UserProfileSkills
from django import forms
from cities_light.models import Country, Region

class UserProfileForm(ModelForm):
    #docfile = forms.ImageField(label='Choose your picture', help_text='max. 2 megabytes')    
    about_me = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = UserProfile
        fields = ['name','profile_photo','current_status','about_me', 'country', 'region']     
        
    def save(self, **kwargs):
        is_default = kwargs['is_default']
        user_profile = kwargs['instance']
        user = kwargs['user']
        if user_profile is None:
            user_profile = super(UserProfileForm, self).save(commit=False)
            
        user_profile.user=user
        #user_profile.professional_title=self.cleaned_data["professional_title"]
        user_profile.name=self.cleaned_data["name"]
        user_profile.about_me=self.cleaned_data["about_me"]
        user_profile.current_status=self.cleaned_data["current_status"]
        user_profile.profile_photo = self.cleaned_data["profile_photo"]
        user_profile.country = Country.objects.get(pk=self.data["country"])
        user_profile.region = Region.objects.get(pk=self.data["region"])
        if is_default is not None:        
            user_profile.is_default = is_default
        user_profile.display_name = user.first_name + ' ' + user.last_name
        user_profile.name = 'default'        
        user_profile.save()
    
    

class UserProfileCompanyForm(ModelForm):   
    
    class Meta:
        model = UserProfileCompany       
        fields = [ 'company_name', 'industry', 'position_name','worked_from','worked_to'] 
        
    def save(self, **kwargs):
        user_profile_company = kwargs['instance']
        user_profile = kwargs['profile']
        user = kwargs['user']
        if user_profile_company is None:        
            user_profile_company = super(UserProfileCompanyForm, self).save(commit=False)
            
        user_profile_company.profile = user_profile
        user_profile_company.user = user
        user_profile_company.company_name=self.cleaned_data["company_name"]
        user_profile_company.industry=self.cleaned_data["industry"]
        user_profile_company.position_name=self.cleaned_data["position_name"]
        user_profile_company.worked_from=self.cleaned_data["worked_from"]
        user_profile_company.worked_to=self.cleaned_data["worked_to"]        
        user_profile_company.save()
        
class UserProfileEducationForm(ModelForm):    
    class Meta:
        model = UserProfileEducation
        fields = [ 'school_name','studied_from','studied_to', 'field_of_study', 'grade', 'activities', 'descriptin']
            
    def save(self, **kwargs):
        user_profile_education = kwargs['instance']
        user = kwargs['user']
        user_profile = kwargs['profile']
        if user_profile_education is None:        
            user_profile_education = super(UserProfileEducationForm, self).save(commit=False)
            
        user_profile_education.profile = user_profile
        user_profile_education.user = user
        user_profile_education.school_name=self.cleaned_data["school_name"]
        user_profile_education.studied_from=self.cleaned_data["studied_from"]
        user_profile_education.studied_to=self.cleaned_data["studied_to"]
        user_profile_education.field_of_study=self.cleaned_data["field_of_study"]
        user_profile_education.grade=self.cleaned_data["grade"]
        user_profile_education.activities=self.cleaned_data["activities"]
        user_profile_education.descriptin=self.cleaned_data["descriptin"]
        user_profile_education.save()
        
class UserProfileSkillForm(ModelForm):    
    
    class Meta:
        model = UserProfileSkills
        fields = ['skill_name']
        
    def save(self, **kwargs):
        user_profile_skill = kwargs['instance']
        user_profile = kwargs['profile']
        user = kwargs['user']
        if user_profile_skill is None:        
            user_profile_skill = super(UserProfileSkillForm, self).save(commit=False)

        user_profile_skill.profile = user_profile
        user_profile_skill.user = user
        user_profile_skill.skill_name=self.cleaned_data["skill_name"]
        user_profile_skill.save()