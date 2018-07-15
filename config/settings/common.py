# -*- coding: utf-8 -*-
"""
Django settings for Python Nigeria project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ
import pytz
import datetime

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (python_nigeria/config/settings/common.py - 3 = python_nigeria/)
APPS_DIR = ROOT_DIR.path("python_nigeria")

env = environ.Env()

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env("DJANGO_READ_DOT_ENV_FILE", default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path(".env"))
    print("Loading : {}".format(env_file))
    env.read_env(env_file)
    print("The .env file has been loaded. See common.py for more information")

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Useful template tags:
    "django.contrib.humanize",
    # Admin
    "django.contrib.admin",
)
THIRD_PARTY_APPS = (
    "crispy_forms",  # Form layouts
    "account",  # registration
    "easy_thumbnails",
    # "taggit",
    "reversion",
    # "metron",
    "sitetree",
    "waffle",
    "markitup",
    "import_export",
    # pinax
    "pinax.boxes",
    # "pinax.eventlog",
    "pinax.pages",
    "pinax.blog",
    "pinax.images",
    # symposion
    "symposion",
    "symposion.conference",
    "symposion.speakers",
    "symposion.proposals",
    "symposion.reviews",
    "symposion.schedule",
    "symposion.sponsorship",
    "symposion.teams",
    "hijack",
    "compat",
    "hijack_admin",
    # 'captcha',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    "python_nigeria.proposals",
    "python_nigeria.core",
    # Your stuff: custom apps go here
    "python_nigeria.tickets",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # 'django.middleware.security.SecurityMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.DisableCFPMiddleware",
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "python_nigeria.contrib.sites.migrations"}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (("""The Python Nigeria Community""", "hello@pycon.ng"),)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    "default": env.db(
        "DATABASE_URL", default="postgres://postgres:postgres@127.0.0.1/pyconng"
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Africa/Lagos"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Your stuff: custom template context processors go here
                "account.context_processors.account",
                "symposion.reviews.context_processors.reviews",
            ],
        },
    }
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap3"

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (str(APPS_DIR.path("static")),)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    "symposion.teams.backends.TeamPermissionsBackend",
    "account.auth_backends.UsernameAuthenticationBackend",
    "account.auth_backends.EmailAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

# Some really nice defaults
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_LOGIN_URL = LOGIN_URL = "/account/login/"
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False
ACCOUNT_USE_AUTH_AUTHENTICATE = True


def ACCOUNT_USER_DISPLAY(user):
    return user.email


# Symposion settings

CONFERENCE_ID = 1
PROPOSAL_FORMS = {
    "tutorial": "python_nigeria.proposals.forms.TutorialProposalForm",
    "talk-25-min": "python_nigeria.proposals.forms.TalkProposalForm",
    "pydata": "python_nigeria.proposals.forms.TalkProposalForm",
    "talk-45-min": "python_nigeria.proposals.forms.TalkProposalForm",
    "open-space": "python_nigeria.proposals.forms.OpenSpaceProposalForm",
}
# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r"^admin/"

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

PINAX_PAGES_HOOKSET = "config.hooks.PinaxPagesHookSet"
PINAX_BOXES_HOOKSET = "config.hooks.PinaxBoxesHookSet"

# adjust for number of reviews currenly about 1/5 (default: 3)
SYMPOSION_VOTE_THRESHOLD = 6

MARKITUP_SET = "markitup/sets/markdown"
MARKITUP_FILTER = ["symposion.markdown_parser.parse", {}]
MARKITUP_SKIN = "markitup/skins/simple"

THEME_CONTACT_EMAIL = "hello@pycon.us"
PAYSTACK_BASE_URL = "https://api.paystack.co"
PAYSTACK_SECRET_KEY = env(
    "PAYSTACK_SECRET_KEY", default="sk_test_a551e347b4fc7af40b897f1fc217ce3642d1faa7"
)
PAYSTACK_PUBLIC_KEY = env(
    "PAYSTACK_PUBLIC_KEY", default="pk_test_fbc2f1812af67479da1306edc72890e0702f052e"
)

HIJACK_LOGIN_REDIRECT_URL = (
    "/dashboard/"
)  # Where admins are redirected to after hijacking a user
HIJACK_LOGOUT_REDIRECT_URL = (
    "/admin/auth/user/"
)  # Where admins are redirected to after releasing a user
HIJACK_ALLOW_GET_REQUESTS = True

RECAPTCHA_PUBLIC_KEY = env(
    "RECAPTCHA_PUBLIC_KEY", default="6LcXCVAUAAAAAJ91TSqGxTa3klWZkVczL_guXHMN"
)
RECAPTCHA_PRIVATE_KEY = env(
    "RECAPTCHA_PRIVATE_KEY", default="6LcXCVAUAAAAAFOQeqopAJH6_MSPGzMGmnnQUM3G"
)

DEADLINE_DATE = datetime.datetime(2018, 7, 17, 9, tzinfo=pytz.UTC)

