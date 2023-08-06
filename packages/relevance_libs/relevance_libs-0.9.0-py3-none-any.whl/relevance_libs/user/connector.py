"""
This module provides the main interface for connecting to the user API.
"""

import typing
import requests
from werkzeug.exceptions import Unauthorized

from .models import User
from .models import Session


class UserServerConnector():
    """
    The user server connector is used to query the user API for information about
    sessions and users.
    """

    def __init__(self, target: str, token: str = None) -> None:
        """
        The *target* argument is the URI to the user API instance.

        If *token* is supplied, it is used as a master token whenever a token
        is not supplied in the request.
        """
        self.target = target
        self.token = token

    def ping(self) -> dict:
        """
        Ping and obtain server information.
        """
        response = requests.get(self.target)
        response.raise_for_status()
        return response.json()

    def create_session(self, login: str, secret: str) -> Session:
        """
        Create a new session.
        """
        url = '{0}/sessions/'.format(self.target)
        payload = {'email': login, 'secret': secret}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        body = response.json()
        return Session(body)

    def get_session(self, token: str) -> Session:
        """
        Get a session with a specific token.
        """
        if not self.token:
            url = '{0}/sessions/me/'.format(self.target)
            response = requests.get(url, headers={'Authorization': token})
            if response.status_code == 401:
                return None
        else:
            url = '{0}/session/{1}/'.format(self.target, token)
            response = requests.get(url, headers={'Authorization': token})
            if response.status_code == 404:
                return None
            response.raise_for_status()

        body = response.json()
        return Session(body)

    def get_user(self, uid: str = 'me', *, token: str = None) -> User:
        """
        Get a user with a specific UID.

        If *token* is supplied, it is used to authenticate the request, otherwise
        the master token is used instead.
        """
        url = '{0}/users/{1}/'.format(self.target, uid)
        response = requests.get(url, headers={'Authorization': token or self.token})
        response.raise_for_status()
        body = response.json()
        return User(body)

    def get_active_session(self, token: str = None, *,
                           should_raise: bool = True) -> typing.Tuple[Session, User]:
        """
        Get the active session and user for the current Flask request.
        """
        if not token:
            from flask import request  # pylint:disable=import-outside-toplevel
            token = request.headers.get('authorization')

        session = self.get_session(token)
        if session:
            return (session, self.get_user(token=token))

        if should_raise:
            raise Unauthorized('invalid session')

        return (None, None)
