from django.db import models
from cities_light.models import Region, Country
from app.users.models import SiteUser
from south.modelsinspector import timezone
from Pachondi.core.modelbase.models import BaseModel
from django.utils.translation import ugettext as _

class Position(BaseModel):
    title=models.CharField(max_length=100)
    
class Industry(BaseModel):
    name = models.CharField(max_length=100)

class Company(BaseModel):
    name = models.CharField(max_length=100)
    country=models.ForeignKey(Country)
    state=models.ForeignKey(Region)
    industry=models.ForeignKey(Industry)
    created_user=models.ForeignKey(SiteUser, null=True)
    created_date = models.DateTimeField(_('account created date'), default=timezone.now)
    modified_date = models.DateTimeField(_('account modified date'), default=timezone.now)

