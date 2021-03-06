import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'mupy')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

SECRET_KEY = ''

ADMINS = (
    ('example', 'foo@example.org'),
)

DEFAULT_FROM_EMAIL = 'foo@bar.com'

# db connection info
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'mupy.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# handle media and static files serving
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

TIME_ZONE = 'Europe/Athens'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # 'memcached_example': {
    # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    # 'LOCATION': '127.0.0.1:11211',
    # },
}


# how many days should we keep data in the db
DATA_EXPIRES = '2'

MUNIN_NODES = (
    (
        1, {
            'name': 'main',
            'url': 'http://asd.example.org',
            'cgi_path': 'cgi-bin/munin-cgi-graph/',
            'image_path': '',
            'version': 'v1'
        }
    ),
    (
        2, {
            'name': 'extra',
            'url': 'http://extra.example.org',
            'cgi_path': 'cgi-bin/munin-cgi-graph/',
            'image_path': ''
        }
    )
)


AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }

# LDAP CONFIG
# import ldap
# from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# AUTH_LDAP_BIND_DN = ""
# AUTH_LDAP_BIND_PASSWORD = ""
# AUTH_LDAP_SERVER_URI = "ldap://foo.bar.org"
# AUTH_LDAP_START_TLS = True
# AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People, dc=bar, dc=foo",
#             ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
# AUTH_LDAP_USER_ATTR_MAP = {
#         "first_name": "givenName",
#         "last_name": "sn",
#         "email": "mail"
#       }

# # Set up the basic group parameters.
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Groups,dc=foo, dc=bar, dc=org",
#     ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
# )
# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_active": "cn=NOC, ou=Groups, dc=foo, dc=bar, dc=org",
#     "is_staff": "cn=staff, ou=Groups, dc=foo, dc=bar, dc=org",
#     "is_superuser": "cn=NOC, ou=Groups,dc=foo, dc=bar, dc=org"
# }


