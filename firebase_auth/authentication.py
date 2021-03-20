# -*- coding: utf-8 -*-
"""
Authentication backend for handling firebase user.idToken from incoming
Authorization header, verifying, and locally authenticating
"""
from typing import Tuple, Dict
import logging

import firebase_admin
from firebase_admin import auth as firebase_auth
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from rest_framework import (
    authentication,
    exceptions
)

from .settings import api_settings

from . import __title__

from person.models import Person

log = logging.getLogger(__title__)

firebase_credentials = firebase_admin.credentials.Certificate(
    api_settings.FIREBASE_SERVICE_ACCOUNT_KEY
)
firebase = firebase_admin.initialize_app(
    credential=firebase_credentials,
)


class FirebaseAuthentication(authentication.TokenAuthentication):
    """
    Token based authentication using firebase.
    """
    keyword = api_settings.FIREBASE_AUTH_HEADER_PREFIX

    def authenticate_credentials(
        self,
        token: str
    ) -> Tuple[AnonymousUser, Dict]:
        try:
            decoded_token = self._decode_token(token)
            firebase_user = self._authenticate_token(decoded_token)
            local_user = self._get_or_create_local_user(firebase_user)
            return (local_user, decoded_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

    def _decode_token(self, token: str) -> Dict:
        """
        Attempt to verify JWT from Authorization header with Firebase and
        return the decoded token
        """

        try:
            decoded_token = firebase_auth.verify_id_token(
                token,
                check_revoked=api_settings.FIREBASE_CHECK_JWT_REVOKED
            )
            log.info(f'_decode_token - decoded_token: {decoded_token}')
            return decoded_token
        except Exception as e:
            log.error(f'_decode_token - Exception: {e}')
            raise Exception(e)

    def _authenticate_token(
        self,
        decoded_token: Dict
    ) -> firebase_auth.UserRecord:
        """ Returns firebase user if token is authenticated """
        try:
            uid = decoded_token.get('uid')
            log.info(f'_authenticate_token - uid: {uid}')
            firebase_user = firebase_auth.get_user(uid)
            log.info(f'_authenticate_token - firebase_user: {firebase_user}')
            if api_settings.FIREBASE_AUTH_EMAIL_VERIFICATION:
                if not firebase_user.email_verified:
                    raise Exception(
                        'Email address of this user has not been verified.'
                    )
            return firebase_user
        except Exception as e:
            log.error(f'_authenticate_token - Exception: {e}')
            raise Exception(e)

    def _get_or_create_local_user(
        self,
        firebase_user: firebase_auth.UserRecord
    ) -> Person:
        """
        Attempts to return or create a local User from Firebase user data
        """
        log.info(f'_get_or_create_local_user - uid: {firebase_user.uid}')
        person = None
        try:
            person = Person.objects.get(firebase_id=firebase_user.uid)
            log.info(
                f'_get_or_create_local_user - person.is_active: {person.is_active}'
            )
            if not person.is_active:
                raise Exception(
                    'User account is not currently active.'
                )
            person.last_login = timezone.now()
            person.save()
        except Person.DoesNotExist as e:
            log.error(
                f'_get_or_create_local_user - Person.DoesNotExist: {firebase_user.uid}'
            )
            if not api_settings.FIREBASE_CREATE_LOCAL_USER:
                raise Exception('Person is not registered to the application.')

            name = firebase_user.display_name
            if  name is None :
                # if display_name is not exists, name become mail-name
                name = firebase_user.email.split('@')[0]
                
            log.info(
                f'_get_or_create_local_user - name: {name}'
            )
            try:
                person = Person.objects.create(
                    firebase_id=firebase_user.uid,
                    name=name,
                    email=firebase_user.email,
                    email_verified=firebase_user.email_verified,
                    photo_url=firebase_user.photo_url,
                    provider_id=firebase_user.provider_id
                )

                person.save()
            except Exception as e:
                raise Exception(e)
        return person
