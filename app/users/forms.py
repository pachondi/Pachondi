from django.contrib.sites.models import Site
from app.users.settings.models import UserSettings
from app.users.models import SiteUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.template import Context, loader
from django import forms
from django.core.mail import send_mail

class UserSettingsForm(forms.ModelForm):
    #is_activity_broadcast = forms.BooleanField(label="Turn on/off your activity broadcast")
    #broadcast_level = forms.ComboField()
    #network_trace_level =
    
    class Meta:
        model = UserSettings
        fields = ['is_activity_broadcast','broadcast_level']

    def __init__(self, *args, **kwargs):        
        super(UserSettingsForm, self).__init__(*args, **kwargs)        
        
    def save(self, user, commit=True):
        usersettings = super(UserSettingsForm, self).save(commit=False)
        usersettings.user = user      
        usersettings.is_activity_broadcast = self.cleaned_data['is_activity_broadcast']
        
        
        if commit:
            usersettings.save()
            
        return usersettings
            

class UserCreationForm(forms.ModelForm):
    #username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
    #                            help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
    #                            error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    dob = forms.DateField(label="Date of Birth")
    
    email1 = forms.EmailField(label="Email", max_length=75)
    #email2 = forms.EmailField(label="Confirm Email", max_length=75,
    #                         help_text = "Enter your email address again. A confirmation email will be sent to this address.")

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    terms = forms.BooleanField(label="I agree to the terms and conditions")
    #password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
    #                            help_text = "Enter the same password as above, for verification.")
    
    class Meta:
        model = SiteUser
        fields = ()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
    
    def clean_email1(self):
        email1 = self.cleaned_data["email1"]
        users_found = SiteUser.objects.filter(email__iexact=email1)
        if len(users_found) >= 1:
            raise forms.ValidationError("A user with that email already exist.")
        return email1

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1", "")
        email2 = self.cleaned_data["email2"]
        if email1 != email2:
            raise forms.ValidationError("The two email fields didn't match.")
        return email2   
    
    def clean_terms(self):
        terms = self.cleaned_data["terms"]
        if terms == False:
            raise forms.ValidationError("Please read and agree to the terms and conditions.")
        
        return terms
    
    def save(self, commit=True, domain_override=None,
             email_template_name='registration/signup_email.html',
             use_https=False, token_generator=default_token_generator):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email1"]
        user.username = user.email
        user.first_name = self.data["first_name"].strip()
        user.last_name = self.data["last_name"].strip()
        user.dob = self.cleaned_data["dob"]
        user.is_active = True
        user.is_verified = False
        user.user_slug = user.first_name+'.'+user.last_name+'.'+user.dob.isoformat()
        
        
            
        if commit:
            user.save()
            #user.create_settings()
            #user.add_to_network()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            }
        send_mail("Confirmation link sent on %s" % site_name,
                  t.render(Context(c)), 'peyman.gohari@gmail.com', [user.email])
        return user