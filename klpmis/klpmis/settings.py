from django.core.exceptions import ImproperlyConfigured

import os.path

from unipath import Path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = 'support@mahiti.org'

SEND_BROKEN_LINK_EMAILS = True

IGNORABLE_404_ENDS = ('.css', '.html', 'favicon.ico')

ADMINS = (('Sree', 'sree@mahiti.org'), ('RamaKrishna',
          'ramakrishna.marouthu@mahiti.org'), ('Shivangi',
          'shivangi@klp.org.in'), ('Megha', 'megha@klp.org.in'))  # ('Your Name', 'your_email@domain.com'),
PROJECT_ROOT = Path(__file__).ancestor(2)
PYTHON_PATH = 'python'
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

MANAGERS = ADMINS

TESTING = 0
REPORTMAIL_SENDER = 'KLP TEAM <dev@klp.org.in>'
REPORTMAIL_RECEIVER = ['dev@klp.org.in', 'pushparanij@mahiti.org',
                       'megha@klp.org.in']
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'klpmis.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {'autocommit': True},
    }
}

# DEFAULT_FROM_EMAIL = 'support@mahiti.org'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.

# Current Academic Year Month
LAST_MONTH_CUR_ACADEMIC_YEAR = 9
NUM_OF_FLEXI_ANSWER_FORM_RECORDS = 20

USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale

USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = '/home/mahiti/Desktop/emsdev3/static_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/static_media/'
STATIC_URL='/static/'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

ADMIN_MEDIA_PREFIX = '/admin_media/'

# List of callables that know how to import templates from various sources.

TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader')

#     'django.template.loaders.eggs.Loader',

MIDDLEWARE_CLASSES = (  # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fullhistory.fullhistory.FullHistoryMiddleware',
    'schools.middleware.QueryLogMiddleware',
    )

ROOT_URLCONF = 'klpmis.urls'

TEMPLATE_CONTEXT_PROCESSORS = \
    ('django.contrib.auth.context_processors.auth',
     'django.core.context_processors.debug',
     'django.core.context_processors.i18n',
     'django.core.context_processors.media',
     'django.contrib.messages.context_processors.messages')

TEMPLATE_DIRS = '/home/mahiti/Desktop/emsev3/schools/templates/'

INSTALLED_APPS = (  # Uncomment the next line to enable the admin:
                    # 'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'schools',
#    'object_permissions',
    'fullhistory',
    )

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set %s environment variable" % (var_name,)
        raise ImproperlyConfigured(error_msg)
