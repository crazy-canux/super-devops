import logging

from .datamodel import DataModel
from .datacontext import DataContext
from super_devops.utils import BaseUtils


logger = logging.getLogger(__name__)


class BaseYaml(DataContext):
    def __init__(
            self,
            global_conf_file=None,
            *workflow_conf_files
    ):
        self.global_tag = 'global'
        self.local_tag = 'local'
        self.shared_tag = 'shared'

        super(BaseYaml, self).__init__(
            BaseUtils.expandpath(global_conf_file), self.global_tag
        )

        self[self.local_tag] = {}

        if vars(self[self.global_tag]):
            self[self.local_tag] += self[self.global_tag]

        for workflow_conf_file in workflow_conf_files:
            self.update_node_from_file(
                BaseUtils.expandpath(workflow_conf_file), self.local_tag
            )

    @property
    def globals(self):
        return self[self.global_tag]

    @property
    def locals(self):
        return self[self.local_tag]

    @property
    def shared(self):
        return getattr(self[self.local_tag], self.shared_tag, None)

    @shared.setter
    def shared(self, value):
        raise AssertionError('Unreachable setter')

    def __getattr__(self, item):
        if item:
            _val_attribute = getattr(self.locals, item, None) \
                             or getattr(self.shared, item, None)
        else:
            raise AttributeError('Invalid attribute item')
        return _val_attribute or DataModel()
