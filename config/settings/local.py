# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use mailhog for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket
import os
from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['ci.tuteria.com','staging.pycon.ng','localhost']


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='_zmu=w_8zg)a2y+7w=w39rnraick!7r%d!q#jnbxw%59eqh(tk')

# Mail settings
# ------------------------------------------------------------------------------

# EMAIL_PORT = 2201

# EMAIL_HOST = env("EMAIL_HOST", default='127.0.0.1')
# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='PyconNG 2024 <hello@pynigeria.org>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Pycon NG 2024] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ("anymail", )
ANYMAIL = {
    'SENDGRID_API_KEY': env('SENDGRID_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2','ci.tuteria.com','45.32.237.130',
'staging.pycon.ng' ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    'SHOW_TOOLBAR_CALLBACK': 'config.middleware.callback'
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
