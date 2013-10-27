from Pachondi.core.modelbase.models import BaseModel, SiteManager
from django.db import models
from app.users.models import SiteUser
from django.utils.translation import ugettext as _

class UserSettingsManager(SiteManager):
    pass

#is_activity_broadcast : 0-Your activity will not be published, 1-your activity will be published.
#broadcast_level: Restricts who can view your activity.
#connection_access_level: Who can look into your network.
class UserSettings(BaseModel):
    DISCLOSE_IDENTITY_LEVEL=(
                             (1,_('Your Identity')),
                             (2,_('Professional Identity')),
                             (3,_('Anonymous')),
                            )
    ACCESS_LEVEL = ((1,_('Public')), (2,_('Network')), (3,_('Connections')), (4,_('You')))
    
    user = models.OneToOneField(SiteUser, primary_key=True)
    is_activity_broadcast = models.BooleanField(default=True)
    disclose_identity_level = models.PositiveSmallIntegerField(_('How others see you when your view their profile'),
                                               choices=DISCLOSE_IDENTITY_LEVEL, default=0)
    connection_access_level = models.PositiveSmallIntegerField(_('Who can view my connections'),
                                               choices=ACCESS_LEVEL, default=2)    
    broadcast_level = models.PositiveSmallIntegerField(_('Who can see my updates'),
                                               choices=ACCESS_LEVEL, default=3)    
    
    objects = UserSettingsManager()