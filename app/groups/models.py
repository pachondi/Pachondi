import logging
from django.db import models
from app.users.models import SiteUser
from Pachondi.libs.discussions.models import Discussion
from Pachondi.libs.message.models import Message
from Pachondi.core.modelbase.models import BaseModel, SiteManager
from cities_light.models import Country, Region
from django.utils.translation import ugettext as _

log = logging.getLogger(__name__)

class GroupManager(SiteManager):
    pass

class Group(BaseModel):
    GROUP_TYPE=((1,_('Technical')),(2,_('Corporate')))
    #logo = models.ImageField(upload_to='groupimg')
    group_name = models.CharField(max_length=100)
    group_type = models.PositiveSmallIntegerField(_('group type'), choices=GROUP_TYPE)
    summary=models.CharField(max_length=1000)
    description=models.CharField(max_length=2000)
    website=models.CharField(max_length=100)
    owner=models.ForeignKey(SiteUser)
    is_auto_join=models.BooleanField(default=False)
    is_public=models.BooleanField(default=False)
    auto_approve_domains=models.CharField(max_length=100) #domains seperated by semicolon(;)
    language=models.CharField(max_length=100)
    is_region_specific=models.BooleanField(default=False)
    country=models.ForeignKey(Country)
    region=models.ForeignKey(Region)
    _is_active = models.BooleanField(default=True)
    #is_twitter_announcement
    
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
        """
        properties of self.groupdiscussion_set
         __class__, __delattr__, __dict__, __doc__, __format__, __getattribute__, __hash__, __init__,
          __module__, __new__, __reduce__, __reduce_ex__, __repr__, __setattr__, __sizeof__, __str__,
         __subclasshook__  __weakref__  _copy_to_model  _db  _inherited  _insert  _set_creation_counter
         _update  add  aggregate all  annotate  bulk_create complex_filter contribute_to_class
         core_filters count create creation_counter dates  db db_manager defer distinct exclude
         exists  extra  filter get get_empty_query_set get_or_create 
         get_prefetch_query_set get_query_set in_bulk  instance
         iterator latest model none only order_by prefetch_related raw reverse
         select_for_update select_related update  using values values_list        
        """
        """
         _set doesn't 
        """
        rs = [] # create an empty list that will hold the result set
        
        for gd in self.groupdiscussion_set.all():
            irs = (gd,gd.groupdiscussionmessage_set.count())
            # if you don't do this here, 
            # discussions with no messages wont be added
            if gd.groupdiscussionmessage_set.exists() is False:
                #log.debug(gd.groupdiscussionmessage_set.count())
                rs.append(irs) 
            
            for gdm in gd.groupdiscussionmessage_set.all():
                irss = irs + (gdm,) # if messages found for a group
                rs.append(irss) #append the result set to a list.
            
        return rs
        
        #return [(gd_msgs.id,gd_msgs.raw_message,gd_msgs.group_discussion) for gd_msgs in self.groupdiscussion_set.groupdiscussionmessage_set.all()]
    @models.permalink
    def get_absolute_url(self):
        return ('show-group', [str(self.id)])   
        
    def __unicode__(self):
        return self.name + " object"
    
    def __str__(self):
        return self.name + " object"
    
        class Admin:
            pass
        
        class Meta:
            pass


    
class GroupMembers(BaseModel):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(SiteUser)
    is_display_in_profile=models.BooleanField(default=True)
    is_email_all_discussion = models.BooleanField(default=True)
    is_email_digest=models.BooleanField(default=True)
    digest_email_frequency=models.CharField(max_length=100)#Daily, Weekly, Monthly
    is_announcement_emails=models.BooleanField(default=True)
    announcement_email_frequency=models.CharField(max_length=100)#Daily, Weekly, Monthly
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

class GroupType(BaseModel):
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.type
    