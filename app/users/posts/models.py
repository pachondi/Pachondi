import logging
from Pachondi.core.modelbase.models import BaseModel
from django.db import models
from django.utils.datetime_safe import datetime
from app.users.models import SiteUser
log = logging.getLogger(__name__)

class UserPost(BaseModel):
    user = models.ForeignKey(SiteUser)
    message = models.CharField(max_length=2048)
    post_by = models.ForeignKey(SiteUser, related_name='post_by')
    post_dt = models.DateTimeField(default=datetime.now())
    
class PostComment(BaseModel):    
    post = models.ForeignKey(UserPost)    
    message = models.CharField(max_length=2048)
    comment_by = models.ForeignKey(SiteUser)
    commented_dt = models.DateTimeField(default=datetime.now())