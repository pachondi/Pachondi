# Django settings for Pachondi project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': os.path.join(PROJECT_DIR, '../db/pachondi_development'),                      # Or path to database file if using sqlite3.
        'NAME': 'pachondi_development',
        # The following settings are not used with sqlite3:
        #'HOST': 'localhost',
        'USER': 'masteradmin',
        'PASSWORD': 'masteradmin',
        'PORT': '3306',                      # Set to mpty string for default.
        #'TEST_NAME': 'pachondi_test'
    }             
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # This setting defines the additional locations the staticfiles app will 
    # traverse if the FileSystemFinder finder is enabled, e.g. if you use 
    # the collectstatic or findstatic management command or use the static 
    # file serving view. In case you want to refer to files in one of the 
    # locations with an additional namespace, you can optionally provide a 
    # prefix as (prefix, path) tuples,
    
    ("js",os.path.join(PROJECT_DIR, '../static/js')),
)

IMAGE_UPLOAD_PATH='/static/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ux_7+dpvoc2=)2ys65bdn5#bd-ahi#k9xps#ljmv37xj+!&&o9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'Pachondi.urls'

AUTH_PROFILE_MODULE = 'profile.UserProfile'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Pachondi.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # M:\DOCS\GitRep\unchained\groups\templates\groups\form.html (django.template.loaders.app_directories.Loader)
    # os.path.join(PROJECT_DIR, '../<app>/templates'), -> loaded by file system loader for templates
    #os.path.join(PROJECT_DIR, '../groups/templates'),
    #os.path.join(PROJECT_DIR, '../templates'),
    #"M:/DOCS/GitRep/unchained/groups/templates",
    
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # All user created apps
    'Pachondi.core.modelbase',
    #'Pachondi.core.models',
    'Pachondi.libs.discussions',
    'Pachondi.libs.message',    
    'app.users',
    'app.users.authentication',
    'app.users.registration', 
    'app.users.settings',
    'app.users.posts', 
    'app.groups',    
    'app.relationships', 
    'app.profile',
    'app.profile.education', 
    'app.profile.company',    
    'cities_light',
    #'relationships',   
    # South for database migrations
    'south',    
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

SOUTH_TESTS_MIGRATE = False
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },    
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR + "/log/logfiles",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },                         
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        }                          
    },
    'loggers': {
          """
       'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },          
          """      
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'groups': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },                
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'ram.be2005@gmail.com'
EMAIL_HOST_PASSWORD = 'imbzotkavlqmgaua'
EMAIL_USE_TLS = True


AUTH_USER_MODEL = 'users.SiteUser'
LOGIN_REDIRECT_URL = '/users/'
LOGIN_URL = '/users/login'