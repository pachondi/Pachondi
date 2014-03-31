from django.db import models
from django.utils.functional import lazy
from django.utils.translation import ugettext
from django.utils import six
from Pachondi.core.modelbase.models import BaseModel
from app.users.models import SiteUser, SiteUserManager
from cities_light.models import Country, Region
from django.contrib.sites.models import SiteManager
from app.profile.company.models import Company, Position
from app.profile.education.models import School, Degree
from django.utils.translation import ugettext as _
from app.profile.skills.models import Skill

ugettext_lazy = lazy(ugettext, six.text_type)


class UserProfileManager(SiteManager):
    def __init__(self, instance=None, *args, **kwargs):
        super(UserProfileManager, self).__init__(*args, **kwargs)
        self.instance = instance
        
    def has_default_profile(self):
        if self.filter(is_default=True, user=self.instance):
            return True
        return False
        
    def get_default_profile(self):
        p = self.get(is_default=True, user=self.instance)
        return p 
    
    def get_profile(self, profile_id):
        p = self.get(pk=profile_id)
        return p
    
    def get_masked_profiles(self):
        p = self.filter(is_default=False,user=self.instance)
        return p
    
    def get_all_profiles(self):
        p = self.filter(user=self.instance)
        return p
    
    
    def get_all_profiles_by(self, content_type_id, criteria_id):
        if(content_type_id==27):            
            return UserProfile.objects.filter(companies__in = UserProfileCompany.objects.filter(position_id = criteria_id))
    
    
class UserProfileCompanyManager(SiteManager):
    def __init__(self, instance=None, *args, **kwargs):
        super(UserProfileCompanyManager, self).__init__(*args, **kwargs)
        self.instance = instance
        
    def get_companies(self):
        c = UserProfileCompany.objects.filter(profile=self.instance)
        return c

class UserProfileEducationManager(SiteManager):
    def __init__(self, instance=None, *args, **kwargs):
        super(UserProfileEducationManager, self).__init__(*args, **kwargs)
        self.instance = instance
        
    def get_education(self):
        c = UserProfileEducation.objects.filter(profile=self.instance)
        return c

class UserProfileSkillsManager(SiteManager):
    def __init__(self, instance=None, *args, **kwargs):
        super(UserProfileSkillsManager, self).__init__(*args, **kwargs)
        self.instance = instance
        
    def get_skills(self):
        c = UserProfileSkills.objects.filter(profile=self.instance)
        return c

class UserProfile(BaseModel):
    CURRENT_STATUS=(('E', _('Employed')), ('S',_('Student')), ('O',_('Self-Employed')))
    
    user = models.ForeignKey(SiteUser, related_name='userprofiles')
    name=models.CharField(_('profile name'), max_length=100)
    display_name = models.CharField(_('Display Name'), max_length=128)
    profile_photo = models.ImageField(upload_to='profilepic')
    professional_title = models.CharField(_('professional title'), max_length=256)
    about_me = models.CharField(_('about me'), max_length=1000)
    country=models.ForeignKey(Country)
    region=models.ForeignKey(Region)
    current_status=models.CharField('What are you currently?',choices=CURRENT_STATUS, default='E', max_length=1)    
    is_default = models.BooleanField(default=False)
    
    objects=UserProfileManager()
    
    class Meta:
        verbose_name = _('userprofile')
        verbose_name_plural = _('userprofiles')
        
    def __unicode__(self):
        return self.name  
    
    def total_experience(self):
        total_exp = 0 
        for experience in self.companies.all():
            total_exp += (experience.worked_to - experience.worked_from).days/365
            
        return total_exp
    
class UserProfileCompany(BaseModel):
    user = models.ForeignKey(SiteUser)
    profile = models.ForeignKey(UserProfile, related_name='companies')
    company = models.ForeignKey(Company, blank=True, null=True)
    company_name = models.CharField(max_length=100)
    #Location
    industry=models.CharField(max_length=100)
    position = models.ForeignKey(Position,blank=True, null=True)
    position_name = models.CharField(max_length=100)
    worked_from=models.DateField()
    worked_to=models.DateField()
        
    objects=UserProfileCompanyManager()
    
    class Meta:
        verbose_name = _('usercompany')
        verbose_name_plural = _('usercompanies')
        
    def __unicode__(self):
        return self.company_name  
    
class UserProfileEducation(BaseModel):
    user = models.ForeignKey(SiteUser)
    profile = models.ForeignKey(UserProfile, related_name='schools')
    school = models.ForeignKey(School,blank=True, null=True)
    school_name = models.CharField(max_length=100)
    #Location
    studied_from=models.DateField()
    studied_to=models.DateField()
    degree = models.ForeignKey(Degree,blank=True, null=True)
    field_of_study = models.CharField(max_length=100)
    grade=models.CharField(max_length=100)
    activities=models.CharField(max_length=100)
    descriptin=models.CharField(max_length=100)
    
    objects=UserProfileEducationManager()
    
    class Meta:
        verbose_name = _('usereducation')
        verbose_name_plural = _('usereducations')
    
class UserProfileSkills(BaseModel):
    profile = models.ForeignKey(UserProfile, related_name='skills')    
    user = models.ForeignKey(SiteUser)
    skill = models.ForeignKey(Skill,blank=True, null=True)
    skill_name = models.CharField(max_length=128)
    #attested_users = models.ManyToManyField() 
    objects=UserProfileSkillsManager()
    
    class Meta:
        verbose_name = _('userskill')
        verbose_name_plural = _('userskills')
    
#For tracking viewers of this profile also viewed data
class ProfileViewHistory(BaseModel):
    viewer = models.ForeignKey(SiteUser)
    viewer_session_id = models.CharField(max_length=100)
    viewed_profile = models.ForeignKey(UserProfile)
