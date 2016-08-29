# Top settings file for development
from .settings import *


DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
]
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
INSTALLED_APPS += (
    'debug_toolbar',
)

# Disable sending mail
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Including a default secret key since this is just for development
SECRET_KEY = environ('SECRET_KEY', u'dipps!+sq49#e2k#5^@4*^qn#8s83$kawqqxn&_-*xo7twru*8')

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
        # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}