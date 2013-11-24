from django.forms.models import ModelForm
from app.profile.models import UserProfile, UserProfileCompany,\
    UserProfileEducation, UserProfileSkills
from django import forms

class UserProfileForm(ModelForm):
    #docfile = forms.ImageField(label='Choose your picture', help_text='max. 2 megabytes')    
    about_me = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = UserProfile
        fields = ['profile_photo','current_status','about_me', 'country', 'region']     
        
    def save(self, request):
        user_profile = super(UserProfileForm, self).save(commit=False)
        user_profile.user=request.user
        #user_profile.professional_title=self.cleaned_data["professional_title"]
        #user_profile.about_me=self.cleaned_data["about_me"]
        #user_profile.current_status=self.cleaned_data["current_status"]
        #user_profile.country = Country.objects.get(pk=self.data["country"])
        #user_profile.region = Region.objects.get(pk=self.data["region"])
        user_profile.is_default = True
        user_profile.display_name = request.user.first_name + ' ' + request.user.last_name
        user_profile.name = 'default'        
        user_profile.save()
    

class UserProfileCompanyForm(ModelForm):   
    
    class Meta:
        model = UserProfileCompany       
        fields = [ 'company_name', 'industry', 'position_name','worked_from','worked_to'] 
        
    def save(self, request):
        user_profile_company = super(UserProfileCompanyForm, self).save(commit=False)
        user_profile_company.profile = request.user.userprofiles.get_default_profile()
        user_profile_company.user = request.user
        #user_profile_company.company_name=self.cleaned_data["company_name"]
        #user_profile_company.industry=self.cleaned_data["industry"]
        #user_profile_company.position_name=self.cleaned_data["position_name"]
        #user_profile_company.worked_from=self.cleaned_data["worked_from"]
        #user_profile_company.worked_to=self.cleaned_data["worked_to"]        
        user_profile_company.save()
        
class UserProfileEducationForm(ModelForm):    
    class Meta:
        model = UserProfileEducation
        fields = [ 'school_name','studied_from','studied_to', 'field_of_study', 'grade', 'activities', 'descriptin']
            
    def save(self, request):
        user_profile_education = super(UserProfileEducationForm, self).save(commit=False)
        user_profile_education.profile = request.user.userprofiles.get_default_profile()
        user_profile_education.user = request.user
        #user_profile_education.school_name=self.cleaned_data["school_name"]
        #user_profile_education.studied_from=self.cleaned_data["studied_from"]
        #user_profile_education.studied_to=self.cleaned_data["studied_to"]
        #user_profile_education.field_of_study=self.cleaned_data["field_of_study"]
        #user_profile_education.grade=self.cleaned_data["grade"]
        #user_profile_education.activities=self.cleaned_data["activities"]
        #user_profile_education.descriptin=self.cleaned_data["descriptin"]
        user_profile_education.save()
        
class UserProfileSkillForm(ModelForm):    
    
    class Meta:
        model = UserProfileSkills
        fields = ['skill_name']
        
    def save(self, request):
        user_profile_skill = super(UserProfileSkillForm, self).save(commit=False)
        user_profile_skill.profile = request.user.userprofiles.get_default_profile()
        user_profile_skill.user = request.user
        #user_profile_skill.skill_name=self.cleaned_data["skill_name"]
        user_profile_skill.save()