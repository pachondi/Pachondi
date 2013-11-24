from Pachondi.core.modelbase.models import BaseModel
from django.db import models
from cities_light.models import Country, Region
from app.users.models import SiteUser
from south.modelsinspector import timezone
from django.utils.translation import ugettext as _

class School(BaseModel):
    name = models.CharField(max_length=100)
    country=models.ForeignKey(Country)
    state=models.ForeignKey(Region)    
    created_user=models.ForeignKey(SiteUser, null=True)
    created_date = models.DateTimeField(_('account created date'), default=timezone.now)
    modified_date = models.DateTimeField(_('account modified date'), default=timezone.now)
    
class Degree(BaseModel):
    pass;



