import os
import logging

import yaml

from .context import Context
from .serializable import serializable
from .datamodel import DataModel


logger = logging.getLogger(__name__)
logging.getLogger('yaml').setLevel(logging.WARNING)


@serializable
class DataContext(Context):
    def __init__(self, ctx=None, node_name='default'):
        self.attributes = []
        self.__dict__['current_node'] = node_name or 'default'

        Context.__init__(self, ctx)
        # super(DataContext, self).__init__(ctx)

    def _initialize_context(self, ctx):
        if ctx:
            if os.path.isfile(os.path.expanduser(str(ctx))):
                self.update_node_from_file(ctx, self.current_node)
            else:
                self.update_node_from_stream(ctx, self.current_node)
        else:
            self.update(self.current_node)

    def update_node_from_file(self, file_path, node_name=None):
        try:
            file_path = os.path.expanduser(file_path)
            node_name = (
                node_name or self.current_node or
                os.path.splitext(os.path.split(file_path)[-1])[0]
            )
            with open(file_path) as stream:
                self.update(node_name, **yaml.load(stream))
        except IOError as e:
            raise e

    def update_node_from_stream(self, stream, node_name=None):
        try:
            node_name = node_name or self.current_node or str(type(stream))
            self.update(node_name, **yaml.safe_load(stream))
        except yaml.YAMLError as e:
            raise e

    def update(self, node_name, **kwargs):
        if not node_name or not issubclass(type(node_name), basestring):
            raise RuntimeError(
                'Node name is unspecified or invalid.'
            )
        if node_name in self.attributes:
            self[node_name] += kwargs
        else:
            self[node_name] = kwargs

    def __setattr__(self, key, value):
        if getattr(value, 'iteritems', None):
            value = DataModel(**value)
        if isinstance(value, DataModel):
            self.__dict__['current_node'] = key
            if key not in self.attributes:
                self.attributes.append(key)
        self.__dict__[key] = value