DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'pyke_app_db'
DATABASE_USER = 'pyke_app_db_user'
DATABASE_PASSWORD = 'pyke_app_db_password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-au'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'supercalafragelisticexpesomethingsomething'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'pyke_django_ask.urls'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites', # required by auth (test suite at least)
    'pyke_django_app.foo',
)
STATIC_DIRS = [
    'static',
]
PYKE_RULES = "knowledge_base"
DIRS_TO_DEPLOY = [
        'knowledge_base'
        ]
TEMPLATE_DIRS = [] 
