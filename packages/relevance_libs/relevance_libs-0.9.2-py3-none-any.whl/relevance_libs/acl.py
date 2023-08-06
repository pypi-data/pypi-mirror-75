"""
This module contains the interface for access control management.
"""

import uuid
import hashlib
import datetime


class AccessManager():
    """
    This manager is used to control and validate access keys. It can be used both
    server-side and client-side.
    """

    def __init__(self, salt: str, *, factor: int = 120, key: str = None) -> None:
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
        self.keys = {}
        if key:
            self.register('default', key)

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

    def register(self, name: str, key: str) -> None:
        """
        Register a new access key.
        """
        self.keys[name] = key

    def create(self, name: str) -> str:
        """
        Create and register a new access key.
        """
        key = str(uuid.uuid4())
        self.register(name, key)
        return key

    def generate_token(self, key: str, data: object = None) -> str:
        """
        Generate a token based on salt and factor given a specific key.
        """
        data = self.stringify(data or '')
        now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        timestamp = int(now.timestamp() / self.factor)
        result = '{0}{1}{2}{3}'.format(key, self.salt, timestamp, data).encode('utf-8')
        return hashlib.sha256(result).hexdigest()

    def validate(self, token: str, data: object = None) -> str:
        """
        Validate a token and return the associated access name.
        """
        for name, key in self.keys.items():
            if token == self.generate_token(key, data):
                return name

        return None


class AccessManagerLoader():
    """
    This class enables one to create access management objects from configuration.
    """

    def create_manager(self, conf: dict) -> AccessManager:
        """
        Create an access manager instance from a configuration dict.
        """
        try:
            salt = conf['salt']
            factor = conf['factor']
            manager = AccessManager(salt, factor=factor)

            for name, key in conf.get('access_keys', {}).items():
                manager.register(name, key)

            return manager

        except KeyError as ex:
            raise KeyError('missing backend configuration key: %s' % ex)
