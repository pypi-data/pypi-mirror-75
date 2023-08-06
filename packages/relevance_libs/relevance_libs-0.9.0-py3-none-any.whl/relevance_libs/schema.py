"""
This module provides the schema protocol and associated interfaces, used for
manipulating and validating object properties at runtime.
"""

import typing
import re
import enum
import hashlib
import pydoc
import dateutil.parser


class SchemaValueError(ValueError):
    """
    Exception raised when a validation error occurs and should_raise is enabled.
    """


class Format(enum.Enum):
    """
    Describes the different property formats.
    """
    EMAIL = 'email'
    REGEX = 'regex'
    DATETIME = 'datetime'
    MD5 = 'md5'
    SHA1 = 'sha1'
    SHA256 = 'sha256'
    SHA512 = 'sha512'


class Flags(enum.Enum):
    """
    Additional flags that can be passed to the property.
    """
    REQUIRED = 'required'
    TRIM = 'trim'
    UPPERCASE = 'uppercase'
    LOWERCASE = 'lowercase'


class Property():
    """
    The property class contains the metadata for a schema property.
    """

    def __init__(self, datatype: type, *, fmt: Format = None,
                 default: object = NotImplemented,
                 expr: typing.Union[str, 'Property', 'Schema'] = None,
                 flags: typing.List[Flags] = None, salt: str = 'abc123',
                 name: str = None) -> None:
        """
        Initialize a property.
        """
        self.datatype = datatype
        self.fmt = Format(fmt) if fmt else None
        self.default = default
        self.expr = expr
        self.flags = [Flags(x) for x in (flags or [])]
        self.salt = salt
        self.name = name

    @property
    def is_required(self) -> bool:
        """
        Check whether a property is required or not.
        """
        return Flags.REQUIRED in self.flags

    def validate(self, value: object, *, apply_format: bool = True,
                 should_raise: bool = True) -> bool:
        """
        Validate a value against the property and raise an exception on error.
        """
        # pylint: disable=too-many-branches

        if ((value is None or
             (isinstance(value, str) and value.strip() == '') or
             (not isinstance(value, (int, float, bool)) and not value))):
            if self.is_required:
                raise ValueError('a value is required')
            return False

        if not isinstance(value, self.datatype):
            want = self.datatype.__name__
            got = value.__class__.__name__
            if should_raise:
                raise ValueError('data type does not match, expected "%s" got "%s"' % (want, got))
            return False

        if apply_format:
            value = self.format(value)

        is_valid = True

        if self.fmt == Format.EMAIL:
            is_valid = re.match(r'[a-z0-9_\.+-]+@[a-z0-9\.-]+', value) is not None
        if self.fmt == Format.REGEX:
            is_valid = re.match(self.expr, str(value)) is not None
        if self.fmt == Format.DATETIME:
            try:
                dateutil.parser.parse(value)
                is_valid = True
            except Exception:
                is_valid = False
        if self.fmt == Format.MD5:
            is_valid = re.match(r'^[a-f0-9]{32}$', value) is not None
        if self.fmt == Format.SHA1:
            is_valid = re.match(r'^[a-f0-9]{40}$', value) is not None
        if self.fmt == Format.SHA256:
            is_valid = re.match(r'^[a-f0-9]{64}$', value) is not None
        if self.fmt == Format.SHA512:
            is_valid = re.match(r'^[a-f0-9]{128}$', value) is not None

        if not is_valid:
            if should_raise:
                raise ValueError('value has invalid format')
            return False

        if issubclass(self.datatype, list) and value and self.expr:
            for item in value:
                if not self.expr.validate(item, should_raise=should_raise):
                    return False

        if issubclass(self.datatype, dict) and value and self.expr:
            for item in value.values():
                if not self.expr.validate(item, should_raise=should_raise):
                    return False

        return True

    def format(self, value: object) -> object:
        """
        Format a value based on the input format.
        """
        # pylint: disable=line-too-long

        if ((value is None or
             (isinstance(value, str) and value.strip() == '') or
             (not isinstance(value, (int, float, bool)) and not value))):
            if self.is_required:
                raise ValueError('a value is required')
            return None

        try:
            result = self.datatype(value) if self.datatype is not object else value
        except ValueError:
            raise ValueError('data type does not match')

        if Flags.TRIM in self.flags:
            result = value.strip()
        if Flags.LOWERCASE in self.flags:
            result = value.lower()
        if Flags.UPPERCASE in self.flags:
            result = value.upper()
        if self.fmt == Format.EMAIL:
            result = value.lower().strip()
        if self.fmt == Format.DATETIME:
            result = dateutil.parser.parse(value).isoformat()
        if self.fmt == Format.MD5 and not self.validate(value, apply_format=False, should_raise=False):
            result = hashlib.md5((self.salt + value).encode('utf-8')).hexdigest()
        if self.fmt == Format.SHA1 and not self.validate(value, apply_format=False, should_raise=False):
            result = hashlib.sha1((self.salt + value).encode('utf-8')).hexdigest()
        if self.fmt == Format.SHA256 and not self.validate(value, apply_format=False, should_raise=False):
            result = hashlib.sha256((self.salt + value).encode('utf-8')).hexdigest()
        if self.fmt == Format.SHA512 and not self.validate(value, apply_format=False, should_raise=False):
            result = hashlib.sha512((self.salt + value).encode('utf-8')).hexdigest()

        return result


class Schema():
    """
    The *Schema* class is used to validate and map dictionary objects based on a
    specific set of fields.
    """

    def __init__(self, properties: typing.Dict[str, Property], *, name: str = None) -> None:
        """
        Initialize the schema.

        The *name* is a unique name for the schema type.

        The *properties* is a mapping of field names and their attributes.
        """
        self.properties = properties
        self.name = name

    def __getitem__(self, key: str) -> Property:
        """
        Get a specific property object.
        """
        return self.properties[key]

    def format(self, target: dict, properties: typing.List[str] = None) -> None:
        """
        Format a target dictionary's properties to match the schema.

        This method formats in-place and does not return a copy of the original
        object.
        """
        for key, value in target.items():
            if properties and key not in properties:
                continue
            if key not in self.properties:
                continue
            target[key] = self.properties[key].format(value)

        for key, prop in self.properties.items():
            if prop.default is not NotImplemented and key not in target:
                target[key] = prop.default

    def validate(self, target: dict, properties: typing.List[str] = None, *,
                 ignore_unknown: bool = False,
                 should_raise: bool = False) -> typing.List[typing.Tuple[str, Exception]]:
        """
        Validate an object against the schema.

        Invoking this method will validate the *target* object against the schema,
        returning a list of tuples containing the name of the field and an exception
        object that caused an error. If the method returns an empty list, the object
        is considered a valid one.

        The *properties* argument allow to select specific property names to validate. If
        omitted, all properties are validated.

        If *ignore_unknown*, if extra fields that were not defined are passed, an
        error will not be raised.

        If *should_raise* is enabled, the method will raise an exception at the first
        encountered error.
        """
        results = []

        for key, prop in self.properties.items():
            if properties and key not in properties:
                continue

            try:
                value = target.get(key)
                prop.validate(value)
            except Exception as ex:
                if should_raise:
                    raise SchemaValueError('%s[%s] (%s): %s' % (
                        self.name or '', key, ex.__class__.__name__, str(ex),
                    ))
                results.append((key, ex))

        if not ignore_unknown:
            keys = list(self.properties.keys())
            for key in target.keys():
                try:
                    if key not in keys:
                        raise KeyError('unknown property "%s"' % (key))
                except Exception as ex:
                    if should_raise:
                        raise SchemaValueError('%s[%s] (%s): %s' % (
                            self.name or '', key, ex.__class__.__name__, str(ex),
                        ))
                    results.append((key, ex))

        return results


class SchemaLoader():
    """
    Factory class for creating schemas based on configuration dictionaries.
    """

    def load_property(self, value: dict, *, name: str = None) -> Property:
        """
        Load a property object from a configuration dictionary.
        """
        datatype = str
        fmt = None
        expr = None
        flags = None
        default = NotImplemented

        if isinstance(value, str):
            try:
                fmt = Format(value)
            except ValueError:
                datatype = pydoc.locate(value)

        else:
            datatype = pydoc.locate(value.get('datatype', 'str'))
            fmt = Format(value['format']) if 'format' in value else None
            expr = value.get('expr')
            default = value.get('default', NotImplemented)
            flags = [Flags(x) for x in value.get('flags', [])]

        if datatype is None:
            raise TypeError('invalid datatype for "%s"' % name)

        if expr and (isinstance(expr, dict) or issubclass(datatype, (list, dict))):
            expr = self.load_property(expr, name=datatype.__class__.__name__)

        return Property(datatype, fmt=fmt, expr=expr, flags=flags, default=default)

    def load_config(self, conf: dict, *, name: str = None) -> Schema:
        """
        Load a schema from a configuration dictionary.
        """
        properties = {}

        for key, value in conf.items():
            properties[key] = self.load_property(value, name=key)

        result = Schema(properties, name=name)
        return result

    def load_config_map(self, items: dict, *, prefix: str = None) -> typing.Dict[str, Schema]:
        """
        Load a dictionary of schemas.
        """
        results = {}

        for key, conf in items.items():
            data = dict(conf)
            name = '{0}:{1}'.format(prefix, key) if prefix else key
            results[key] = self.load_config(data, name=name)

        return results
