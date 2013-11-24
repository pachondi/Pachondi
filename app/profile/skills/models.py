from Pachondi.core.modelbase.models import BaseModel
from django.db import models

class Skill(BaseModel):
    name = models.CharField(max_length=128)
    

    