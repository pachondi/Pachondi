from django.forms.models import ModelForm
from app.users.settings.models import UserSettings

class UserSettingsForm(ModelForm):
    #is_activity_broadcast = forms.BooleanField(label="Turn on/off your activity broadcast")
    #broadcast_level = forms.ComboField()
    #network_trace_level =
    
    class Meta:
        model = UserSettings
        fields = ['is_activity_broadcast', 'disclose_identity_level', 'broadcast_level','connection_access_level']

    def __init__(self, *args, **kwargs):        
        super(UserSettingsForm, self).__init__(*args, **kwargs)        
        
    def save(self, user, commit=True):
        usersettings = super(UserSettingsForm, self).save(commit=False)
        usersettings.user = user      
        usersettings.is_activity_broadcast = self.cleaned_data['is_activity_broadcast']
        usersettings.disclose_identity_level = self.cleaned_data['disclose_identity_level']
        
        if commit:
            usersettings.save()
            
        return usersettings
            