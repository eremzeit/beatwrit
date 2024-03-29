# Django settings for beatwrit project.
from sitesettings import *

ADMINS = (
     ('Alan Jones', 'admin@beatwrit.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''



# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z)263(c)yq!#1z#7yr5lqim0rcl9dm^ev@2kh@fn-$+=l)o4&8'


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
)

TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.request",
"django.contrib.messages.context_processors.messages",
'beatwrit.context_processors.log',
'beatwrit.context_processors.sqlinfo',
)


ROOT_URLCONF = 'beatwrit.urls'

INSTALLED_APPS = (	
	'beatwrit.main',
    'beatwrit.lib.django_cron',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
)


############################
###    GLOBAL SETTINGS  ####
############################
LOGIN_REDIRECT_URL = '/profile'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_HOST = 'mail.beatwrit.com'
EMAIL_PORT = 25
EMAIL_HOST_USER  = 'accounts@beatwrit.com'
EMAIL_HOST_PASSWORD = 'R2P9AntR'
#EMAIL_USE_TLS
DEFAULT_FROM_EMAIL = 'account@beatwrit.com'

CRON_POLLING_FREQUENCY = 600

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'beatwrit.tokens.TokenAuthenticationBackend',
) 


"""
Mailbox Login: reminders@beatwrit.com (use the whole thing!)
Password: ?ag^Sz^k

Mailbox Login: accounts@beatwrit.com (use the whole thing!)
Password: R2P9AntR

"""

"""
Facebook App
App Name:   Beatwrit
App URL:    beatwrit.com/
App ID: 138127262900823
App Secret: c28bb05bc8d4f4811636a171e78a2069"""

"""
ReCaptcha
domain: beatwrit.com
public: 6LcAfb0SAAAAAGnc6V2pUINygy16u23i8v7vt6l_
private: 6LcAfb0SAAAAADpvgNDfQRf9xiRgydHHtd3IxRaC

domain: global.beatwrit.com
public: 6LccfL0SAAAAAEVaqq0PT3nmmPydfmwSrBBMK2BI
private: 6LccfL0SAAAAAOhYkdVo5fNr5FUXabMZP2XlIsVw 

"""
