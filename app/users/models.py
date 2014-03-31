from django.db import models
from Pachondi.core.modelbase.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from south.modelsinspector import timezone
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from taggit.managers import TaggableManager
from app.users.handler import UserConnectionHandler

class SiteUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = SiteUserManager.normalize_email(email)
        user = self.model(email=email, is_active=True, is_verified=False,
                          last_login=now, created_date=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)        
        u.is_admin=True
        u.save(using=self._db)
        return u

    
 
class SiteUser(AbstractBaseUser, PermissionsMixin):
   
    
    email = models.EmailField(_('email address'),
        max_length=255,
        unique=True,
        db_index=True,
        )
    first_name = models.CharField(_('First Name'), max_length=128, error_messages={'blank':_("First name cannot be empty")})
    last_name = models.CharField(max_length=128, null=True)
    user_slug = models.CharField(max_length=128)
    dob=models.DateField(_('Date of birth'))
    website=models.CharField(_('Website'), max_length=256)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    invalid_attempts = models.IntegerField(default=0)
    lock_expires_on = models.DateTimeField(null=True);
    
    is_show_viewers_also_viewed = models.BooleanField(default=False)
    created_date = models.DateTimeField(_('account created date'), default=timezone.now)
    modified_date = models.DateTimeField(_('account modified date'), default=timezone.now)
    
    objects = SiteUserManager()    
    tags=TaggableManager()
    connections = UserConnectionHandler()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']
    
    class Meta:
        verbose_name = _('siteuser')
        verbose_name_plural = _('siteusers')
 
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

 
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
 
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin
    
    def get_absolute_url(self):
        return "/users/%s/" % self.user_slug
    
    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
        

    
class UserEmail(BaseModel):
    user = models.ForeignKey(SiteUser)
    email = models.EmailField(_('email address'),
        max_length=255,
        unique=True,
        )
    is_verified=models.BooleanField(default=False)
    is_primary=models.BooleanField(default=False)
    
class UserWebsites(BaseModel):
    user = models.ForeignKey(SiteUser)
    type = models.CharField(max_length=50)
    website = models.CharField(_('website'),
        max_length=255
        )
    


class UserRecommendation(BaseModel):
    RECOMMEND_AS = (
                    (1,_('Colleague')), 
                    (2, _('Student')), 
                    (3, _('Business official')),
                    )
    user = models.ForeignKey(SiteUser)
    message = models.CharField(max_length=2000)    
    recommender = models.ForeignKey(SiteUser, related_name='recommended_by')
    recommended_as = models.IntegerField(_('recommended as'), choices=RECOMMEND_AS)
    recommend_basis = models.CharField(max_length=256)
    recommender_title = models.CharField(max_length=256)
    user_title = models.CharField(max_length=256)
    created_date = models.DateTimeField()
 
    
    
    