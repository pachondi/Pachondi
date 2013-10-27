from django.forms.models import ModelForm
from app.profile.models import UserProfile
from cities_light.models import Country, Region

class UserProfileForm(ModelForm):
    #docfile = forms.ImageField(label='Choose your picture', help_text='max. 2 megabytes')    

    class Meta:
        model = UserProfile
        fields = ['country','region']     
        
    def save(self,user):
        user_profile = super(UserProfileForm, self).save(commit=False)
        user_profile.user=user
        user_profile.country = Country.objects.get(pk=self.data["country"])
        user_profile.region = Region.objects.get(pk=self.data["region"])
        user_profile.save()
        