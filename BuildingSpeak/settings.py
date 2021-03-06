# Django settings for BuildingSpeak project.
import os
import django
# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('David Ashley', 'dashley@drydenengineering.com'),
    #('Jesse Dovi',   'jdovi@drydenengineering.com'),

)

MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
if 'heroku' in DJANGO_ROOT:
    ALLOWED_HOSTS = ['.buildingspeak-staging.herokuapp.com',
                     '.buildingspeak-staging.com',
                     '.buildingspeak-production.herokuapp.com',
                     '.buildingspeak-production.com',
                     ]
else:
    ALLOWED_HOSTS = ['.buildingspeak-staging.herokuapp.com',
                     '.buildingspeak-staging.com',
                     '.buildingspeak-production.herokuapp.com',
                     '.buildingspeak-production.com',
                     '127.0.0.1',
                     ]

###
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'US/Eastern'

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''


if 'heroku' in DJANGO_ROOT:
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
else: #even locally, use S3 as long as internet is available
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#else: #to work locally without internet, use this line instead
#    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if 'heroku' in DJANGO_ROOT:
    STATIC_ROOT = '/static/'
else:
    STATIC_ROOT = '/static/'
#else: #won't generally collect locally, but if we do, collect to here
#    STATIC_ROOT = 'C:/Users/dashley/Desktop/Dryden/BuildingSpeak/static/'
    
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if 'heroku' in DJANGO_ROOT:
    STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
else: #still use S3 when developing locally; if no internet, comment out and use the next else
    STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
#else:  #use this to at least pull css/js/etc. from local folder when no internet available
#    STATIC_URL = '/static/'
    
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = '51^-45as5jxejwjr+m!put_jy!xpnzvbncj@a6f$z19x39&amp;l6t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'BuildingSpeakApp.models.UserRestrictMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MANDRILL_APIKEY = os.environ.get('MANDRILL_APIKEY')
MANDRILL_USERNAME = os.environ.get('MANDRILL_USERNAME')
SEND_BROKEN_LINK_EMAILS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = MANDRILL_USERNAME
EMAIL_HOST_PASSWORD = MANDRILL_APIKEY
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = 'admin@buildingspeak.com'
DEFAULT_FROM_EMAIL = 'admin@buildingspeak.com'

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

LOGIN_URL = '/login'

ROOT_URLCONF = 'BuildingSpeak.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'BuildingSpeak.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'BuildingSpeakTemplates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'BuildingSpeakApp',
    'storages',
)


#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
if 'dashley' in SITE_ROOT:
    bsapp_handlers =  []#['console', 'logfile']    ['logfile']
else:
    bsapp_handlers = []
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug': {
            'format' : "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt' : "%H:%M:%S"
        },
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
#        'logfile': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': 'C:/Users/dashley/Box Sync/BuildingSpeak/BuildingSpeakApp/logfile.txt',
#            'maxBytes': 10000000,
#            'backupCount': 2,
#            'formatter': 'debug',
#        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'BuildingSpeakApp': {
            'handlers': bsapp_handlers,
            'level': 'DEBUG',
            'propagate': False,
        },
        
    }
}


# Parse database configuration from $DATABASE_URL
if 'heroku' in DJANGO_ROOT:
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] =  dj_database_url.config()
else:
    import ast
    DATABASES = ast.literal_eval(os.environ.get('LOCAL_DJANGO_DATABASE'))