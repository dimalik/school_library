# -*- coding: utf-8 -*-

# Django settings for library project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Athens'
LANGUAGE_CODE = 'el-GR'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

ADMINS = (
    ('Dimitrios Alikaniotis', 'dim.alikaniotis@gmail.com'),
)

MANAGERS = ADMINS

SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'
MEDIA_ROOT = '/media/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BUILDOUT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'o$ops!nw9%bb6^k=guw^q#vzrq(f+@4=v+8g6i9*#2-+2@yi+p'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
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

ROOT_URLCONF = 'library.urls'

WSGI_APPLICATION = 'library.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BUILDOUT_DIR, 'templates'),
    os.path.join(BUILDOUT_DIR, 'templates', 'bookshelf'),
    os.path.join(BUILDOUT_DIR, 'templates', 'library'),
    os.path.join(BUILDOUT_DIR, 'templates', 'lists'),
    os.path.join(BUILDOUT_DIR, 'templates', 'userena'),
    )

INSTALLED_APPS = (
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    )
    
INSTALLED_APPS += (
    'djangoratings',
    'taggit',
    'taggit_autocomplete_modified',
    'haystack',
    'tinymce',
    'guardian',
    'userena',
    'easy_thumbnails',
    'ajax_select',
    'import_export',
    'bootstrap3',
    'reversion',
    'widget_tweaks',
    'scribbler',
    'django_object_actions',
    )

INSTALLED_APPS += (
    'watson',
    'transactions',
    'bookshelf',
    'lists',
    'reservations',
    'accounts',
    'assignments',
    'presentations',
    'suggestions',
    )

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dim.alikaniotis@gmail.com'
EMAIL_HOST_PASSWORD = 'dhq4432tmb'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'item'  : {'model':'bookshelf.item', 'search_field':'title'},
    'author': {'model':'bookshelf.author', 'search_field': 'name'}
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

LOGIN_URL = '/'
#AUTH_USER_MODEL = 'accounts.MyProfile'
AUTH_PROFILE_MODULE = 'accounts.Profile'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}


TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,xhtmlxtras,paste,searchreplace,",
    'theme': "advanced",
    "theme_advanced_buttons3_add": "cite,abbr",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'theme_advanced_buttons4' : 'fontselect, fontsizeselect, forecolor, backcolor',
    
}

#AUTH_USER_MODEL = 'users.MyUser'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend', # this is default
)

ANONYMOUS_USER_ID = -1
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
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
SUIT_CONFIG = {
    'ADMIN_NAME': u'Διαχείριση βιβλιοθήκης 1ου Πειραματικού',
    'HEADER_DATE_FORMAT': 'l, j. F Y', # Saturday, 16th March 2013
    'HEADER_TIME_FORMAT': 'H:i',       # 18:42
    'SEARCH_URL': '/admin/bookshelf/item',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU_ICONS': {
            'sites': 'icon-leaf',
            'auth': 'icon-lock',
        },
    'MENU_EXCLUDE': ('sites',
        'transactions.transaction',
        'lists.booklist',
        'reservations.reservation',
        'assignments.assignment',
        'presentations.inpresentation',
        'suggestions.suggestion',
        'auth.user',
        'auth.group',
        'accounts.profile',
        ),
    'MENU': (
        '-',
        {'app': 'bookshelf', 'label': u'Βιβλιοθήκη'},
        {'app': 'lists', 'label': u'Λίστες βιβλίων'},
        {'app': 'transactions', 'label': u'Δανεισμοί βιβλίων'},
        {'app': 'reservations', 'label': u'Κρατήσεις'},
        {'app': 'assignments', 'label': u'Εργασίες'},
        '-',
        {'app': 'presentations', 'label': u'Παρουσιάσεις'},
        {'app': 'suggestions', 'label': u'Προτάσεις'},
        '-',
        {'app': 'auth', 'icon':'icon-user', 'label': u'Λογαριασμοί'},
        {'app': 'accounts', 'label': u'Προφίλ'},
        '-',
    )
}
try:
    from localsettings import *
  #  from debugtoolbarsettings import *
   # INSTALLED_APPS += INSTALLED_APPS_2
 #   MIDDLEWARE_CLASSES += MIDDLEWARE_CLASSES_2
except ImportError:
    pass
