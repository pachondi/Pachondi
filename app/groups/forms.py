from django.forms import ModelForm
from app.groups.models import Group, GroupType

#http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['group_name','group_type','summary',
                  'description']
        #fields = [ field.name for field in Group.get_editable_fields(Group()) ]
        #fields = ["name","description"]
        '''
        fields = "__all__" # all fields (ommitting will do the same in 1.6)
        exclude = [] # list of all fields  same as above
         if you set editable=False on the model field, any form created 
         from the model via ModelForm will not include that field.
        '''
        
class GroupAdminSettingsForm(ModelForm):
    class Meta:
        model = Group
        fields = ['owner','language_default','group_type',
                  'auto_approve_domains','is_auto_join',
                  'is_public','is_region_specific']