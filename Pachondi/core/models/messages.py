from Pachondi.core.modelbase.models import BaseModel

# Abstract discussion class.
class Message(BaseModel):
    pass

    class Meta:
        abstract = True