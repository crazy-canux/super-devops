import copy
import os
import logging
import six

import yaml


try:
    basestring
except Exception:
    basestring = str

logger = logging.getLogger(__name__)
logging.getLogger('yaml').setLevel(logging.WARNING)


def serializable(cls):

    class SerializableCls(yaml.YAMLObject, cls):
        yaml_tag = '!{tag}'.format(tag=cls.__name__)

        def __init__(self, *args, **kwargs):
            yaml.YAMLObject.__init__(self)
            cls.__init__(self, *args, **kwargs)
            # super(SerializableCls, self).__init__(*args, **kwargs)

        def dump(self, path):
            try:
                data = copy.deepcopy(self)
                # for key, value in vars(self).iteritems():
                for key, value in six.iteritems(vars(self)):
                    if hasattr(value, '__dict__') and (
                            not isinstance(value, yaml.YAMLObject)
                    ):
                        delattr(data, key)

                with open(path, 'w') as stream:
                    yaml.dump(data, stream)
            except IOError as e:
                raise e
            except yaml.YAMLError as e:
                raise e
            except Exception as e:
                raise RuntimeError(e)

        @staticmethod
        def load(path):
            if not os.path.isfile(path):
                raise IOError('Invalid file path.')
            try:
                with open(path, 'r') as stream:
                    model = yaml.load(stream, yaml.SafeLoader)
            except IOError as e:
                model = e
            except yaml.YAMLError:
                model = yaml.YAMLObject
            except Exception as e:
                raise e
            return model

    return type(
        cls.__name__,
        (SerializableCls,),
        dict(SerializableCls.__dict__)
    )
