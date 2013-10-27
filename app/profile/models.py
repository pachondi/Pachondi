from django.db import models
from django.utils.functional import lazy
from django.utils.translation import ugettext
from django.utils import six
from Pachondi.core.modelbase.models import BaseModel
from app.users.models import SiteUser, UserSkills
from cities_light.models import Country, Region
from django.contrib.sites.models import SiteManager
from app.profile.company.models import UserCompany
from app.profile.education.models import UserEducation
from django.utils.translation import ugettext as _

ugettext_lazy = lazy(ugettext, six.text_type)


class UserProfileManager(SiteManager):
    pass

class UserProfile(BaseModel):
    CURRENT_STATUS=(('E', _('Employed')), ('S',_('Student')))
    
    user = models.ForeignKey(SiteUser)
    name=models.CharField(_('profile name'), max_length=100)
    display_name = models.CharField(_('Display Name'), max_length=128)
    profile_photo = models.ImageField(upload_to='profilepic')
    professional_title = models.CharField(_('professional title'), max_length=256)
    about_me = models.CharField(_('about me'), max_length=1000)
    country=models.ForeignKey(Country)
    region=models.ForeignKey(Region)
    current_status=models.CharField('What are you currently?',choices=CURRENT_STATUS, default='E', max_length=1)    
    is_default = models.BooleanField(default=False)
    
    object=UserProfileManager()
    
    class Meta:
        verbose_name = _('siteuserprofile')
        verbose_name_plural = _('siteusersprofile')
        
    def __unicode__(self):
        return self.name  
    
class UserProfileCompany(BaseModel):
    profile = models.ForeignKey(UserProfile)
    company = models.ForeignKey(UserCompany)
    
class UserProfileEducation(BaseModel):
    profile = models.ForeignKey(UserProfile)
    education = models.ForeignKey(UserEducation)
    
class UserProfileSkills(BaseModel):
    profile = models.ForeignKey(UserProfile)
    skill = models.ForeignKey(UserSkills)
    
#For tracking viewers of this profile also viewed data
class ProfileViewHistory(BaseModel):
    viewer = models.ForeignKey(SiteUser)
    viewer_session_id = models.CharField(max_length=100)
    viewed_profile = models.ForeignKey(UserProfile)
     