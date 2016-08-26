"""
Django settings for pyconng project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ as environmental

env = environmental.Env()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = environmental.Path(__file__) - 2  # (crosscheck/config/settings.py - 2 = crosscheck/)
APPS_DIR = ROOT_DIR.path('pyconng')

empty = object()
def environ(key, default=empty):
    try:
        return os.environ[key]
    except KeyError:
        if default is empty:
            raise RuntimeError('environment variable "%s" does not exist' % (key))
        return default


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qxl(3u+8%bb079sy%=^wxu5@)h68+hw#s_e6-lv3#n1^z^e4nm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get("GONDOR_INSTANCE_DOMAIN"),
    "2016.djangocon.us",
    "www.djangocon.us",
    "localhost',"
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "django.contrib.sites",
    'django.contrib.staticfiles',

    # external
    "account",
    "crispy_forms",
    # "easy_thumbnails",
    # "taggit",
    # "reversion",
    # "metron",
    "sitetree",
    "waffle",
    "markitup",
        
    # pinax
    "pinax.boxes",
    # "pinax.eventlog",
    "pinax.pages",
    # "pinax.blog",
    
    # symposion
    "symposion",
    "symposion.conference",
    "symposion.speakers",
    "symposion.proposals",
    "symposion.reviews",
    "symposion.schedule",
    "symposion.sponsorship",
    "symposion.teams",

    # project
    "pyconng.proposals",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DATABASE_URL', default='postgres://postgres:postgres@127.0.0.1/pyconng'),
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': environ("DB_NAME"),
#         'USER': environ("DB_USER"),
#         'PASSWORD': environ("DB_PASSWORD"),
#         'HOST': environ("DB_HOST"),
#         'PORT': environ("DB_PORT"),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = str(APPS_DIR('media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = str(ROOT_DIR('staticfiles'))


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here,
                "account.context_processors.account",
                "symposion.reviews.context_processors.reviews",
                'config.context_processors.consts',
            ],
        },
    },
]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_LOGIN_URL = LOGIN_URL = '/account/login/'
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False
ACCOUNT_USE_AUTH_AUTHENTICATE = True
ACCOUNT_USER_DISPLAY = lambda user: user.email

AUTHENTICATION_BACKENDS = [
    "symposion.teams.backends.TeamPermissionsBackend",
    "account.auth_backends.UsernameAuthenticationBackend",
]

# Symposion settings

CONFERENCE_ID = 1
PROPOSAL_FORMS = {
    "tutorial": "djangocon.proposals.forms.TutorialProposalForm",
    "talk-25-min": "djangocon.proposals.forms.TalkProposalForm",
    "talk-45-min": "djangocon.proposals.forms.TalkProposalForm",
    "open-space": "djangocon.proposals.forms.OpenSpaceProposalForm",
}
PINAX_PAGES_HOOKSET = "config.hooks.PinaxPagesHookSet"
PINAX_BOXES_HOOKSET = "config.hooks.PinaxBoxesHookSet"

# adjust for number of reviews currenly about 1/5 (default: 3)
SYMPOSION_VOTE_THRESHOLD = 6

MARKITUP_SET = "markitup/sets/markdown"
MARKITUP_FILTER = ["symposion.markdown_parser.parse", {}]
MARKITUP_SKIN = "markitup/skins/simple"

THEME_CONTACT_EMAIL = 'hello@djangocon.us'

ADMINS = [
    ('DjangoCon US Errors', 'errors@defna.org'),
]

MANAGERS = [
    ('DjangoCon US', 'hello@djangocon.us'),
]

SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = "DjangoCon US 2016 <noreply@djangocon.us>"

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIGRATION_MODULES = {
    'sites': 'pyconng.contrib.sites.migrations'
}
# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

FIXTURE_DIRS = [
    str(ROOT_DIR('fixtures')),
]
