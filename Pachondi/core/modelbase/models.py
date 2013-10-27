from django.db import models
from django.db.models.manager import Manager

"""
    Base which directly inherits from models which will be used to create all models.
    All basic validations, audit tracking needs to be taken care here.  
"""
class SiteManager(Manager):
    pass

class BaseModel(models.Model):    
    class Meta:
        abstract = True