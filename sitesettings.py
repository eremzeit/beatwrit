
###########################
###    LOCAL SETTINGS  ####
###########################
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'beatwrit',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'inter219',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


TEMPLATE_DIRS = (
    '/home/erem/beatwrit.com/templates/'
)

DOMAIN_STR = '127.0.0.1:8000'
LOCAL_DEVELOPMENT = True
STATIC_DOC_ROOT = '/home/erem/beatwrit.com/files/'
