"""
This module contains the models for the user API connector.
"""

import datetime
import dateutil.parser


class User(dict):
    """
    The model class used to represent users.
    """

    def __repr__(self) -> str:
        """
        Get a human readable object representation
        """
        return '<{0}{1}>'.format(self.__class__.__name__, dict(self))

    def __hash__(self) -> int:
        """
        Get the unique object identifier.
        """
        return self['hash']

    @property
    def uid(self) -> object:
        """
        Get the user identifier.
        """
        return self['id']

    @property
    def login(self) -> str:
        """
        Get the user's login.
        """
        return self.email

    @property
    def email(self) -> str:
        """
        Get the user's email.
        """
        return self['email']

    @property
    def secret(self) -> str:
        """
        Get the user's secret.
        """
        return self['secret']

    @property
    def created_at(self) -> datetime.datetime:
        """
        Get creation date.
        """
        try:
            value = self.get('created_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def updated_at(self) -> datetime.datetime:
        """
        Get modification date.
        """
        try:
            value = self.get('updated_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def expires_at(self) -> datetime.datetime:
        """
        Get the expiration date.
        """
        try:
            value = self.get('expires_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def is_expired(self) -> bool:
        """
        Whether the object is expired or not.
        """
        if not self.expires_at:
            return False
        return datetime.datetime.now() >= self.expires_at

    @property
    def pending_email(self) -> str:
        """
        Get the pending email address.
        """
        return self['email_pending']

    @property
    def confimed_at(self) -> datetime.datetime:
        """
        Get the confirmation date.
        """
        try:
            value = self.get('confirmed_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def is_confirmed(self) -> bool:
        """
        Get the confirmation status.
        """
        return not self.pending_email


class Session(dict):
    """
    The model class used to represent users.
    """

    def __repr__(self) -> str:
        """
        Get a human readable object representation
        """
        return '<{0}{1}>'.format(self.__class__.__name__, dict(self))

    def __hash__(self) -> int:
        """
        Get the unique object identifier.
        """
        return self['hash']

    @property
    def token(self) -> str:
        """
        Get the session token.
        """
        return self['token']

    @property
    def user_id(self) -> str:
        """
        Get the user for the session.
        """
        return self['user_id']

    @property
    def length(self) -> int:
        """
        Get the length of the session.
        """
        return self['length']

    @property
    def created_at(self) -> datetime.datetime:
        """
        Get creation date.
        """
        try:
            value = self.get('created_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def updated_at(self) -> datetime.datetime:
        """
        Get modification date.
        """
        try:
            value = self.get('updated_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def expires_at(self) -> datetime.datetime:
        """
        Get the expiration date.
        """
        try:
            value = self.get('expires_at')
            return dateutil.parser.parse(value)
        except Exception:
            return None

    @property
    def is_expired(self) -> bool:
        """
        Whether the object is expired or not.
        """
        if not self.expires_at:
            return False
        return datetime.datetime.now() >= self.expires_at
