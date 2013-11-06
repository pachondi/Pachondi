import logging
from Pachondi.core.modelbase.models import BaseModel
from django.db import models
log = logging.getLogger(__name__)


# Create your models here.

class Message(BaseModel):
    is_active = models.BooleanField(default=True,null=False,blank=False)

    class Meta:
        abstract = True
        

 