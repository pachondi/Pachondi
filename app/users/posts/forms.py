from django.forms import ModelForm
from app.groups.models import GroupDiscussionMessage



class GroupDiscussionMessageForm(ModelForm):
    class Meta:
        model = GroupDiscussionMessage
        fields = ["id","raw_message","group_discussion"]
        #fields = ["name","description"]
        '''
        fields = "__all__" # all fields (ommitting will do the same in 1.6)
        exclude = [] # list of all fields  same as above
         if you set editable=False on the model field, any form created 
         from the model via ModelForm will not include that field.
        '''