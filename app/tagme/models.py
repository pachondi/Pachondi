"""
This app will be used to make any Model (and hence its instances) taggable.
Idea is that if the model is extended or manager is included
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from app.tagme.utils import tag_parser



import pdb

class Tag(models.Model):
    """
    Giving some personality to tag
    """
    name = models.CharField(verbose_name=_('Name'),unique=True,max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'),unique=True,max_length=100)
    
    """
    def save(self, *args, **kwargs):
        
        @todo:Need to modify self to make sure that only unique tag names and or slugs
        are written to the database. By doing this, it becomes very easy to 
        maintain. And all operations should be silent. All errors resolved
        internally and no errors thrown
        
        try:
            return super(Tag,self).save(*args, **kwargs)
        except IntegrityError:
            return
      """  
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class TaggedItem(models.Model):
    #https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-related-name
    tag = models.ForeignKey(Tag,related_name="%(app_label)s_%(class)s_related")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = ("tag","content_type","object_id")
    
    # On Python 3: def __str__(self):
    def __str__(self):
        return self.tag

class TagHelper(object):
    
    def __get__(self, obj, objtype):
        """
        Oh the sweet mother of everything that is pure!
        http://docs.python.org/2/howto/descriptor.html
        what a concept!
        """
        tag_manager = TagManager(instance=obj,model=objtype) 
        return tag_manager

class TagManager(models.Manager):
        
    def __init__(self,instance,model):
        self.instance = instance
        self.model = model    
        
    def add(self,tags):
        unique_tags = tag_parser(tags)
        return
        #Check if any of the tags are already present
        for tag in unique_tags:
            created_tag, is_new = Tag.objects.get_or_create(name=tag,slug=tag)
            try:
                tag_item = TaggedItem.objects.create(tag=created_tag,content_object=self.instance)
            except IntegrityError:
                pass
            else:    
                tag_item.save()
    