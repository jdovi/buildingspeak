# Django settings for BuildingSpeak project.
import os
import django
# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('David Ashley', 'dashley@drydenengineering.com'),

)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.buildingspeak-staging.herokuapp.com',
                 '.buildingspeak-staging.com',
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


STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#DRA: seems this would be the heroku folder, but since S3 is used, this seems unused
STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#DRA: whatever is in local BuildingSpeakApp/static/ folder gets dumped here
STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

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
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#SEND_BROKEN_LINK_EMAILS = True
#EMAIL_HOST = 'oxmail.registrar-servers.com'
#EMAIL_HOST_USER = 'dashley@drydenengineering.com'
#EMAIL_HOST_PASSWORD = 'Dryden030211!'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_PORT = 26
#EMAIL_USE_TLS = True
#SERVER_EMAIL = 'dashley@drydenengineering.com'

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
#    'django_nose',
#    'django_tables2',
#    'selectable',
    'south',
    'BuildingSpeakApp',
    'storages',
    #'schedule',
#    'rtropo',
#    'rapidsms',
#    'rapidsms.backends.database',
#    'rapidsms.contrib.handlers',
#    'rapidsms.contrib.httptester',
#    'rapidsms.contrib.messagelog',
#    'rapidsms.contrib.messaging',
#    'rapidsms.contrib.registration',
    #'rapidsms.contrib.echo',
#    'rapidsms.contrib.default',  # Must be last
)

#INSTALLED_BACKENDS = {
#    "message_tester": {
#        "ENGINE": "rapidsms.backends.database.DatabaseBackend",
#    },
#    "my-tropo-backend": {
#        "ENGINE": "rtropo.outgoing.TropoBackend",
#        'config': {
#            # Your Tropo application's outbound token for messaging
#            'messaging_token': '2576cf832793f3448cf4d38fca55018eb6131477b66f94d699008083ab23e6935c536e64efc7049b18cfc7c3',
#            # Your Tropo application's voice/messaging phone number (including country code)
#            'number': '+1-678-541-8217',
#        },
#    },
#}

#RAPIDSMS_HANDLERS = (
#    #'rapidsms.contrib.echo.handlers.echo.EchoHandler',
#    'rapidsms.contrib.echo.handlers.ping.PingHandler',
#)

#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
