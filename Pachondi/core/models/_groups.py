from django.db import models
from app.users.models import SiteUser
from Pachondi.libs.discussions.models import Discussion
from Pachondi.libs.message.models import Message
from Pachondi.core.modelbase.models import BaseModel, SiteManager
from cities_light.models import Country, Region

class GroupManager(SiteManager):
    pass

class Group(BaseModel):
    GROUP_TYPE=((1,_('Technical')),(2,_('Corporate')))
    #logo = models.ImageField()
    group_name = models.CharField()
    group_type = models.CharField('',GROUP_TYPE)
    summary=models.CharField(max_length=1000)
    description=models.CharField(max_length=2000)
    website=models.CharField()
    owner=models.ForeignKey(SiteUser)
    is_auto_join=models.BooleanField(default=False)
    is_public=models.BooleanField(default=False)
    auto_approve_domains=models.CharField() #domains seperated by semicolon(;)
    language=models.CharField()
    is_region_specific=models.BooleanField(default=False)
    country=models.ForeignKey(Country)
    region=models.ForeignKey(Region)
    _is_active = models.BooleanField(default=True)
    #is_twitter_announcement
    
class GroupMembers(BaseModel):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(SiteUser)
    is_display_in_profile=models.BooleanField(default=True)
    is_email_all_discussion = models.BooleanField(default=True)
    is_email_digest=models.BooleanField(default=True)
    digest_email_frequency=models.CharField()#Daily, Weekly, Monthly
    is_announcement_emails=models.BooleanField(default=True)
    announcement_email_frequency=models.CharField()#Daily, Weekly, Monthly
    is_allow_member_messages=models.BooleanField(_('Allow members of this group to send me messages'),default=True)
    
class GroupDiscussion(Discussion):
    name = models.CharField(max_length=30)
    group = models.ForeignKey(Group)
    created_by = models.ForeignKey(SiteUser)

    def get_discussions_for_parent(self,g_id):
        return [ (discussion.id, discussion.name) for discussion in self.objects.filter(group=g_id) ]  
    
    def __unicode__(self):
        return self.name+ " object"
    
    def __str__(self):
        return self.name+" object"

        class Admin:
            pass
        
        class Meta:
            pass
        
     
class GroupDiscussionMessage(Message):
    raw_message = models.CharField(max_length=100)
    group_discussion = models.ForeignKey(GroupDiscussion, related_name="for_group")
    linked_message = models.ForeignKey('self',related_name="for_reply",null=True,blank=True)
    
    
    def get_messages_for_parent(self,gd_id):
        return [ (messages.id, messages.raw_message, messages.linked_message) for messages in self.objects.filter(group_discussion=gd_id,is_active=True) ]  
    
    def __unicode__(self):
        return str(self.id) + "- " + self.raw_message + " object"
    
    def __str__(self):
        return str(self.id) + "- " + self.raw_message +" object"
    
        class Admin:
            pass
        
        class Meta:
            pass