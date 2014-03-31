from __future__ import unicode_literals
from django.db import models, connections
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import BaseUserManager
from django.db.models.query import QuerySet


class BaseConnectionManager(BaseUserManager):     
        
    def __init__(self, model, instance):        
        self.model = model
        self.instance=instance
        self._db=None
        
    def establish_symmetrical_connection(self):
        pass
    
    def establish_asymmetrical_connection(self):
        pass
    
    def get_all_connections(self, conn_type):
        result = Connection.objects.get_by_source_or_target(self.instance, conn_type)
        connections = [ c.source_object for c in result if c.source_object != self.instance ]
        connections += [ c.target_object for c in result if c.target_object != self.instance ]        
        return connections
        
    def get_all_target(self):
        return Connection.objects.get_by_target(self.instance).active_connections()
    
    def get_all_source(self):
        return Connection.objects.get_by_source(self.instance).active_connections()
    
    def get_all_active_connections_with(self, target_object):
        return Connection.objects.get_all_connections_between(self.instance, target_object).active_connections()
    
    def get_all_inactive_connections_with(self, target_object):
        return Connection.objects.get_all_connections_between(self.instance, target_object).inactive_connections()
    
    def create(self, target_object, conn_type):
        return Connection.objects.create(source_object=self.instance, 
                                  target_object=target_object, 
                                  connection_type = conn_type
                                  )
    
class ConnectionTypeManager(models.Manager):
    """
    def add(self):
        return self.get_query_set().get(type='add')
    
    def follow(self):
        return self.get_query_set().get(type='follow')

    def block(self):
        return self.get_query_set().get(type='block')
    """
    def get_for_connection(self, conn_type):
        return self.get_query_set().get(type=conn_type) # -> connection type object
    
        

class ConnectionManager(models.Manager):
    
    def get_query_set(self):
        return ConnectionQuerySet(self.model)
    
    def get_by_source(self, filter_object):
        content_type = ContentType.objects.get_for_model(filter_object)
        return self.get_query_set().filter(source_id=filter_object.id,
                                                                source_content_type = content_type
                                                                )
        
    def get_by_target(self, filter_object):
        content_type = ContentType.objects.get_for_model(filter_object)
        return self.get_query_set().filter(target_id=filter_object.id,
                                                                target_content_type = content_type
                                                                )
                
    def get_by_source_or_target(self, filter_object, conn_type):
        content_type = ContentType.objects.get_for_model(filter_object)        
        return self.get_query_set().filter(
                                            (Q(source_id=filter_object.id, 
                                               source_content_type = content_type
                                               ) | 
                                             Q(target_id=filter_object.id, 
                                               target_content_type=content_type)
                                             ),
                                            connection_type=conn_type)        

    def get_all_connections_between(self, a, b):
        a_content_type = ContentType.objects.get_for_model(a)
        b_content_type = ContentType.objects.get_for_model(b)
        return  self.get_query_set().filter(
                                                                Q(source_id=a.id, 
                                                                   source_content_type = a_content_type,
                                                                   target_id = b.id,
                                                                   target_content_type = b_content_type
                                                                   ) | 
                                                                 Q(target_id=a.id, 
                                                                   target_content_type = a_content_type,
                                                                   source_id=b.id,
                                                                   source_content_type = b_content_type,
                                                                   )
                                                                )
        
            
                                           
class ConnectionQuerySet(QuerySet):
    
    def active_connections(self):
        return self.filter(is_active=True)   
    
    def inactive_connections(self):
        return self.filter(is_active=False)
    
    def blockable(self):
        return self.filter(connection_type = ConnectionType.objects.block())
    
    def notblockable(self):
        return self.filter(~Q(connection_type = ConnectionType.objects.block()))
    
    def followable(self):
        return self.filter(connection_type = ConnectionType.objects.follow())
    
    def befriendable(self):
        return self.filter(connection_type = ConnectionType.objects.add())
            
        
class ConnectionType(models.Model):
    type = models.CharField(max_length=100, unique=True)
    is_symmetrical = models.BooleanField(default=False)
    objects = ConnectionTypeManager()
    
    def __unicode__(self):
        return self.type
    
class ConnectionTypeMap(models.Model):
    content_type = models.ForeignKey(ContentType)
    connection_type = models.ForeignKey(ConnectionType)
    
class Connection(models.Model):    
    source_id = models.IntegerField(verbose_name=_('Source id'), db_index=True)
    source_content_type = models.ForeignKey(ContentType, related_name='source')
    target_id = models.IntegerField(verbose_name=_('Target id'), db_index=True)
    target_content_type = models.ForeignKey(ContentType, related_name='target')
    connection_type = models.ForeignKey(ConnectionType)
    is_active = models.BooleanField(default=False)
    source_object = GenericForeignKey('source_content_type','source_id')
    target_object = GenericForeignKey('target_content_type','target_id')    
    objects = ConnectionManager()
    
    def inactivate(self):
        self.is_active = False
        self.save()
    
    def activate(self):
        self.is_active = True
        self.save()
        
    def unblock(self):
        self.delete()    
    
class Relationship(models.Model):
    name = models.CharField(max_length=100, unique=True)
  
class ConnectionRelationship(models.Model):
    connection = models.ForeignKey(Connection)
    related_as = models.ForeignKey(Relationship, related_name='relationships')