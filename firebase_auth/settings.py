# -*- coding: utf-8 -*-
""" Settings config for the drf_firebase_auth application """
import os

from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'FIREBASE_AUTH', None)

DEFAULTS = {
    # path to JSON file with firebase secrets
    'FIREBASE_SERVICE_ACCOUNT_KEY':
        os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY', ),
    # allow creation of new local user in db
    'FIREBASE_CREATE_LOCAL_USER':
        os.getenv('FIREBASE_CREATE_LOCAL_USER', True),
    # commonly JWT or Bearer (e.g. JWT <token>)
    'FIREBASE_AUTH_HEADER_PREFIX':
        os.getenv('FIREBASE_AUTH_HEADER_PREFIX', 'JWT'),
    # verify that JWT has not been revoked
    'FIREBASE_CHECK_JWT_REVOKED':
        os.getenv('FIREBASE_CHECK_JWT_REVOKED', True),
    # require that firebase user.email_verified is True
    'FIREBASE_AUTH_EMAIL_VERIFICATION':
        os.getenv('FIREBASE_AUTH_EMAIL_VERIFICATION', False),
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)