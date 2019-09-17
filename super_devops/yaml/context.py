import logging
import six

logger = logging.getLogger(__name__)

try:
    basestring
except Exception:
    basestring = str


class Context(object):
    def __init__(self, ctx=None):
        super(Context, self).__init__()

        if issubclass(type(ctx), Context):
            self.__iadd__(ctx)
        else:
            self._initialize_context(ctx)

    def _initialize_context(self, ctx):
        raise NotImplementedError(
            'Specific context initialization process not implemented.'
        )

    def __getitem__(self, item):
        return self.__dict__.get(item, None)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __iadd__(self, other):
        if getattr(other, '__dict__', None):
            other = vars(other)
        # if getattr(other, 'iteritems', None):
        # if getattr(six.iteritems(other), 'iteritems', None):
        if getattr(other, 'items', None):
            # for key, value in other.iteritems():
            for key, value in six.iteritems(other):
                self.__update_node(self, key, value)
        else:
            raise ValueError(
                'The argument {} is invalid.'.format(other)
            )
        return self

    def __iter__(self):
        # return vars(self).itertiems()
        return six.iteritems(vars(self))

    def __update_node(self, node, key, value):
        if not getattr(node, key, None) or isinstance(value, basestring):
            if node is self:
                self.__dict__[key] = value
            else:
                setattr(node, key, value)
        else:
            if getattr(value, '__dict__', None):
                value = vars(value)
            # if getattr(value, 'iteritems', None):
            # if getattr(six.iteritems(value), 'iteritems', None):
            if getattr(value, 'items', None):
                # for _key, _value in value.iteritems():
                for _key, _value in six.iteritems(value):
                    self.__update_node(
                        getattr(node, key), _key, _value
                    )
            else:
                self.__dict__[key] += value
