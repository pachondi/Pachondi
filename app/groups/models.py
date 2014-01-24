import logging
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

from app.users.models import SiteUser
#from app.discussions.models import Discussion
#from app.message.models import Message
from Pachondi.core.modelbase.models import BaseModel, SiteManager
#from Pachondi.core.models.discussions import Discussion
#from Pachondi.core.models.messages import Message
from cities_light.models import Country, Region

log = logging.getLogger(__name__)
import pdb

class GroupManager(SiteManager):
    pass

class Group(BaseModel):
    GROUP_TYPE=((1,_('Technical')),(2,_('Corporate')))
    #logo = models.ImageField(upload_to='groupimg')
    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(_('group type'), choices=GROUP_TYPE)
    summary=models.CharField(max_length=1000)
    description=models.CharField(max_length=2000)
    language_default=models.CharField(max_length=100,blank=True)
    owner=models.ForeignKey(SiteUser,null=False)
    country=models.ForeignKey(Country,null=True,blank=True)
    region=models.ForeignKey(Region,null=True,blank=True) #should be zipcode
    website=models.CharField(max_length=100,blank=True)
    auto_approve_domains=models.CharField(max_length=100,blank=True) #domains seperated by semicolon(;)
    is_auto_join=models.BooleanField(default=False)
    is_public=models.BooleanField(default=False)
    is_region_specific=models.BooleanField(default=False)
    _is_active = models.BooleanField(default=True)
    _is_official = models.BooleanField(default=False)
    #is_twitter_announcement
    #_is_official
    
    def get_object_data(self):
        return dict([(field.name,self._get_FIELD_display(field)) for field in self.__class__._meta.fields])
    
    def get_editable_fields(self):
        return [field for field in self.__class__._meta.fields]
     
    def get_group_discussions(self, discussion_id=None):
        # Get related discussions for this group. Thanks to
        # http://stackoverflow.com/questions/4611340/an-issue-filtering-related-models-inside-the-model-definition
        return [(group_discussions.id,group_discussions) for group_discussions in self.groupdiscussion_set.all()]
         
    def get_messages_for_discussions(self,message_id=None):
        """
        data is returned as array of messages for each discussion
        possibly a json dumps needs to be done for async
        requests. So need a common function that dumps 
        a. json object, b. xml
        """
        displayable_discussions = self.get_group_discussions()
        
        for i in range(len(displayable_discussions)):
            #displayable_messages =  gobj.groupdiscussionmessage_set.all()
            disc_id, disc_obj  = displayable_discussions[i]
            message_list = disc_obj.groupdiscussionmessage_set.filter(is_active=True)
            displayable_discussions[i] = (disc_id, disc_obj, message_list)
        
        return displayable_discussions    
    
    def get_group_discussions_with_messages(self):
        rs = [] # create an empty list that will hold the result set
        
        for gd in self.groupdiscussion_set.all():
            irs = (gd,gd.groupdiscussionmessage_set.count())
            allm = []
            for gdm in gd.groupdiscussionmessage_set.all():
                #get message counts
                likes = GroupDiscussionMessageVote.objects.filter(message=gdm).annotate(total_likes = models.Count('user'))
                allm.append((gdm,likes))
            irs = irs + (allm,)
            rs.append(irs)      
        
        return rs
        
        #return [(gd_msgs.id,gd_msgs.raw_message,gd_msgs.group_discussion) for gd_msgs in self.groupdiscussion_set.groupdiscussionmessage_set.all()]
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('group-show', [str(self.id)])   
        
    def __unicode__(self):
        return self.name + " object"
    
    def __str__(self):
        return self.name + " object"
    
        class Admin:
            pass
        
        class Meta:
            pass


def init_groupmember_after_group_create(sender, instance, created, **kwargs):
    """
    A signal to automatically put an entry into GroupMember model
    as soon as a user creates a group. Unable to handle such a 
    situation in view for now as I do not know how to obtain
    a lazy object for group. Even then, handling business logic
    at model level makes sense
    """
    if created:
        groupmember = GroupMember.objects.create(group=instance,
                                                   user=SiteUser.objects.get(id=instance.owner.id),
                                                   is_member_moderator = True, #a owner is automatically a mod
                                                   is_member_owner = True
                                                   )
        
        groupmember.save()

"""
if sender not sent, the signal will fire for every save 
and instance.attribute won't be available properly
"""        
post_save.connect(init_groupmember_after_group_create, sender=Group)    

class GroupMember(BaseModel):
    group = models.ForeignKey(Group, editable=False)
    user = models.ForeignKey(SiteUser, editable=False)
    digest_email_frequency=models.CharField(max_length=100, blank=True)#Daily, Weekly, Monthly
    announcement_email_frequency=models.CharField(max_length=100, blank=True)#Daily, Weekly, Monthly
    is_member_moderator=models.BooleanField(default=False)
    is_member_owner=models.BooleanField(default=False)
    is_display_in_profile=models.BooleanField(default=True)
    is_email_all_discussion = models.BooleanField(default=False)
    is_email_digest=models.BooleanField(default=False)
    is_announcement_emails=models.BooleanField(default=False)
    is_allow_member_messages=models.BooleanField(_('Allow members of this group to send me messages'),default=True)


class GroupDiscussion(BaseModel):
    name = models.CharField(max_length=30)
    group = models.ForeignKey(Group)
    created_by = models.ForeignKey(SiteUser)

    def __unicode__(self):
        return self.name+ " object"
    
    def __str__(self):
        return self.name+" object"

        class Admin:
            pass
        
        class Meta:
            pass

class GroupDiscussionMessage(BaseModel):
    message = models.TextField()
    group = models.ForeignKey(Group)
    discussion = models.ForeignKey(GroupDiscussion)
    linked_message = models.ForeignKey('self',null=True,blank=True)
    created_by = models.ForeignKey(SiteUser)
    

class GroupDiscussionMessageVote(BaseModel):
    message = models.ForeignKey(GroupDiscussionMessage)
    user = models.ForeignKey(SiteUser)


"""    
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
    raw_message = models.CharField(max_length=100,blank=True)
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

class GroupType(BaseModel):
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.type
""" 