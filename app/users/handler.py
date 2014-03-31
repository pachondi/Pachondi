from app.connections.models import BaseConnectionManager, ConnectionType,\
    ConnectionTypeManager


class UserConnectionHandler(object):
    
    def __get__(self, instance, model):        
        cm = UserConnectionManager(model, instance)
        return cm
    
class UserConnectionTypeManager(ConnectionTypeManager):
    def add(self):
        return self.get_for_connection('add')
    
    def follow(self):
        return self.get_query_set().get(type='follow')

    def block(self):
        return self.get_query_set().get(type='block')

class UserConnectionManager(BaseConnectionManager):
    
    def __init__(self, instance, model):
        super(UserConnectionManager, self).__init__(instance, model)
    
    def friends(self):
        conn_type = ConnectionType.objects.get_for_connection('add')
        return self.get_all_connections(conn_type)
    
    def friends_of_friends(self):
        connections = self.friends()  
        first_level_connections = []       
        for c in connections:
            if c.connections is not None:
                for i in c.connections.friends():
                    if i != self.instance:
                        first_level_connections += [i]                                            
        return first_level_connections
    
        
    def followers(self):        
        """
        Give all entities following self
        """
        return self.get_all_target().followable()        
    
    def following(self):    
        """
        Give all entities whom self is following
        """    
        return self.get_all_source().followable()
    
    def blocking(self):
        return self.get_all_target().blockable()
    
    def add(self, target_object):
        inactive_connections = self.get_all_inactive_connections_with(target_object).befriendable()
        
        if inactive_connections.count() == 0:
            self.create(target_object, ConnectionType.objects.get_for_connection('add'))
        else:
            for c in inactive_connections:
                if self.instance != c.source_object:
                    c.activate()
                else:
                    print 'pending request.'
        
    def follow(self, target_object):                
        conn_type = self.connection_types.follow() 
        self.create(target_object, conn_type)
    
    def block(self,target_object):
        """
        While blocking, existing relationship, if exists, should be removed
        An entity A can block entity B even if no connection exists
        Blocking creates a connection
        """
        """
        @todo: create unique on source, target and connection type. Exception handling while create.
         
        """
        """
        Inactivate existing connections
        """
        active_connections = self.get_all_active_connections_with(target_object).notblockable()
        for ac in active_connections:
            ac.inactivate()
        
        """
        create a blocking relationship
        """
        conn_type = self.connection_types.block()
        c = self.create(target_object, conn_type)
        c.activate()
        

    def unblock(self,target_object):
        """
        Delete a blocking relationship, if any
        """
        active_blocked_connections = self.get_all_active_connections_with(target_object).blockable()
        
        for abc in active_blocked_connections:
            abc.unblock()
             
        
        """
        Activate inactivated connections 
        """    
        inactive_connections = self.get_all_inactive_connections_with(target_object)
        for ic in inactive_connections:
            ic.activate()