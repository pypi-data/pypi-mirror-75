"""
This module contains the interface for access control management.
"""

import typing
import uuid
import hashlib
import datetime


class SignatureService():
    """
    This service is used to sign request data and validate it against access keys.
    """

    def __init__(self, salt: str, *, factor: int = 120) -> None:
        """
        The *salt* argument is a random string that is used to hash the data
        when matching an access token.

        The *factor* is a number that is used as a factor of the UTC timestamp
        sent in the request. A bigger factor makes time syncronisation errors
        less likely but decreases entropy.

        If *key* is passed in, a default key object will be registered.
        """
        self.salt = salt
        self.factor = factor

    @classmethod
    def stringify(cls, data: object) -> str:
        """
        Stringify arbitrary data.
        """
        parts = []
        if isinstance(data, (list, tuple)):
            parts = [cls.stringify(x) for x in data]

        elif isinstance(data, dict):
            for key, value in data.items():
                parts.append('{0}:{1}'.format(
                    cls.stringify(key),
                    cls.stringify(value),
                ))

        else:
            parts = ['{0}'.format(data)]

        parts.sort()
        return ','.join(parts)

    def sign(self, key: str, data: object = None) -> str:
        """
        Generate a token based on salt and factor given a specific key.
        """
        data = self.stringify(data or '')
        now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        timestamp = int(now.timestamp() / self.factor)
        result = '{0}{1}{2}{3}'.format(key, self.salt, timestamp, data).encode('utf-8')
        return hashlib.sha256(result).hexdigest()

    def validate(self, keys: typing.Dict[str, str], token: str, data: object = None) -> str:
        """
        Validate a token and return the associated access name.
        """
        for name, key in keys.items():
            if token == key or token == self.sign(key, data):
                return name

        return None
