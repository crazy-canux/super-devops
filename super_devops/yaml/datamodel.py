import logging
import six

import yaml

from .serializable import serializable


try:
    basestring
except Exception:
    basestring = str

logger = logging.getLogger(__name__)
logging.getLogger('yaml').setLevel(logging.WARNING)


@serializable
class DataModel(object):
    def __init__(self, **kwargs):
        # for key, value in kwargs.iteritems():
        for key, value in six.iteritems(kwargs):
            self[key] = value

    def __getitem__(self, item):
        if item:
            return getattr(self, item, None)
        else:
            raise AttributeError(
                'Invalid attribute item.'
            )

    def __setitem__(self, key, value):
        # if hasattr(value, 'iteritems'):
        # if hasattr(six.iteritems(value), 'iteritems'):
        if hasattr(value, 'items'):
            value = DataModel(**value)
        # string also have __iter__, should handle list only.
        # elif hasattr(value, '__iter__'):
        elif hasattr(value, '__iter__') and not isinstance(value, basestring):
            node = []
            for item in value:
                # if hasattr(item, 'iteritems'):
                # if hasattr(six.iteritems(item), 'iteritems'):
                if hasattr(item, 'items'):
                    child = DataModel(**item)
                elif isinstance(item, yaml.YAMLObject):
                    child = item
                else:
                    try:
                        child = yaml.safe_load(
                            yaml.safe_dump(item)
                        )
                    except yaml.YAMLError as e:
                        child = e
                node.append(child)
            value = node
        elif isinstance(value, yaml.YAMLObject):
            pass
        else:
            try:
                value = yaml.safe_load(yaml.safe_dump(value))
            except yaml.YAMLError as e:
                value = e
        self.__dict__[key] = value

    def __iadd__(self, other):
        # if getattr(other, 'iteritems', None):
        # if getattr(six.iteritems(other), 'iteritems', None):
        if getattr(other, 'items', None):
            other = DataModel(**other)

        if isinstance(other, type(self)):
            # for key, value in vars(other).iteritems():
            for key, value in six.iteritems(vars(other)):
                if not getattr(self, key, None) or (
                        isinstance(value, basestring) or (value is None)
                ):
                    self.__dict__[key] = value
                else:
                    self.__dict__[key] += value
        else:
            raise ValueError(
                'The argument {} is invalid.'.format(other)
            )
        return self
