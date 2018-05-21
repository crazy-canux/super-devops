import os
import sys
from collections import OrderedDict

from robot.parsing.model import TestData
from robot.api import logger


class Workflow(object):
    def __init__(self, name, doc, tags, steps):
        self.name = name,
        self.doc = doc,
        self.tags = tags,
        self.keywords  = self.__parse_steps(steps)

    def __parse_steps(self, steps):
        keywords = []
        for step in steps:
            if hasattr(step, 'name'):
                if step.args:
                    keywords.append(
                        '{step} {args}'.format(
                            step=step.name,
                            args=str('.'.join(step.args))
                        )
                    )
                else:
                    keywords.append('{step}'.format(step=step.name))
        return keywords


class Suite(object):
    def __init__(self, sources=None):
        self.test_files = []
        self.test_suites = self.__load_test_files(sources)

        self.__workflowdict = None

    def __load_test_files(self, sources):
        if os.path.isfile(sources):
            self.test_files.append(sources)
        else:
            if os.path.isdir(sources):
                for path, _, files in os.walk(sources):
                    self.test_files += [
                        os.path.join(path, file)
                        for file in files
                        if file.endswith('.robot') or
                           file.endswith('.txt') or
                           file.endswith('.html')
                    ]
        if self.test_files:
            return [
                TestData(source=file)
                for file in self.test_files
            ]
        else:
            raise ValueError('No workflow files found.')

    def __transfer_suite_to_workflows(self):
        _dict = OrderedDict()

        for suite in self.test_suites:
            for case in suite.testcase_table:
                _dict[case.name] = Workflow(
                    case.name,
                    case.doc.value,
                    case.tags,
                    case.steps
                )
        return _dict

    @property
    def workflowdict(self):
        """Put all workflow in a order dict.

        :returns __workflowdict: {'workflow_name': 'Workflow object', ...}
        :type __workflowdict: OrderDict
        """
        if not self.__workflowdict:
            self.__workflowdict = self.__transfer_suite_to_workflows()
        return self.__workflowdict

    @property
    def workflowlist(self):
        return [str(key) for key in self.workflowdict.keys()]

    @workflowlist.setter
    def workflowlist(self, value):
        return self.workflowdict.keys().extend(value)

    def get_workflow_name_by_index(self, index=None):
        """Get test case by index in order dict."""
        return self.workflowlist[int(index) - 1]

    def get_workflow_by_name(self, names=None):
        """Get test case by names."""
        _workflowlist = []
        for name in names:
            for case_name in self.workflowlist:
                if name.split('*')[0] in case_name:
                    _workflowlist.append(case_name)
        return _workflowlist

    def get_workflows_by_tags(self, tags=None):
        """Used for robot --include."""
        _workflowlist = []
        for case_name in self.workflowlist:
            if set(
                    [tag.upper() for tag in tags]
            ) & set(
                [
                    tag.upper()
                    for tag in self.workflowdict.get(case_name).tags[0].value
                ]
            ):
                _workflowlist.append(case_name)
        return _workflowlist

    def remove_workflow_by_tags(self, workflowlist, tags=None):
        """Used for robot --exclude."""
        _workflowlist = []
        for case_name in workflowlist:
            if not set(
                    [tag.upper() for tag in tags]
            ) & set(
                [
                    tag.upper()
                    for tag in self.workflowdict.get(case_name).tags[0].value
                ]
            ):
                _workflowlist.append(case_name)
        return _workflowlist


class Output(object):
    def __init__(self, path):
        self.terminal = sys.stdout
        self.path = path
        self.__file = None

    def __enter__(self):
        self.__file = open(self.path, 'w')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__file:
            self.__file.close()
            self.__file = None

    def close(self):
        self.__exit__(None, None, None)

    def write(self, message):
        if not self.__file:
            self.__enter__()
        self.__file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.__file.flush()
        self.terminal.flush()





