"""
This module provides the main interface for connecting to the analytics API.
"""

import requests

from ..acl import AccessManager


class AnalyticsServerConnector():
    """
    The user server connector is used to query the user API for information about
    sessions and users.
    """

    def __init__(self, acl: AccessManager, target: str, *, key_name: str = 'default') -> None:
        """
        The *target* argument is the URI to the user API instance.

        If *token* is supplied, it is used as a master token whenever a token
        is not supplied in the request.
        """
        self.target = target
        self.acl = acl
        self.key_name = key_name

    def ping(self) -> dict:
        """
        Ping and obtain server information.
        """
        response = requests.get(self.target)
        response.raise_for_status()
        return response.json()

    def get_token(self, data: str = None):
        """
        Get an authorization token.
        """
        key = self.acl.keys[self.key_name]
        return self.acl.generate_token(key, data)

    def log_event(self, event_type: str, data: object) -> None:
        """
        Log an event to the server.
        """
        url = '{0}/events/{1}/'.format(self.target, event_type)
        response = requests.post(url, json=data, headers={'Authorization': self.get_token(data)})
        response.raise_for_status()
