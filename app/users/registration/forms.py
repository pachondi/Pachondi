from django import forms
from app.users.models import SiteUser
from django.utils.translation import ugettext as _
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.core.mail import send_mail
from django.template import Context, loader
from django.contrib.sites.models import Site


class RegistrationForm(forms.ModelForm):
    #username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
    #                            help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
    #                            error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
            
    #email1 = forms.EmailField(label=_("Email"), max_length=75)
    #email2 = forms.EmailField(label="Confirm Email", max_length=75,
    #                         help_text = "Enter your email address again. A confirmation email will be sent to this address.")

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput,
                                help_text = _("Enter the same password as above, for verification."))
    terms = forms.BooleanField(label=_("I agree to the terms and conditions"))
    #password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
    #                            help_text = "Enter the same password as above, for verification.")
    
    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'email', 'dob')

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
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
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
        html = t.render(Context(c))
        send_mail("Confirmation link sent on %s" % site_name,
                  html, 'pachondi@gmail.com', [user.email])
        return user
    