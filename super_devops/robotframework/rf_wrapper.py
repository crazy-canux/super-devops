import argparse
import datetime
import os
from argparse import HelpFormatter, Action

import robot
from robot.api import logger
from robot.api import ExecutionResult

from super_devops.misc.colorama_wrapper import BaseColor
from super_devops.utils import BaseUtils
from .utils import Suite, Output


# TODO: write filename in log/debug file.
# TODO: verify arguments.


class BaseRF(object):

    def __init__(
            self,
            source=None,
            output=None,
            prog='robot',
            description='robot framework command customize.',
            epilog='robot framework command options',
            version='0.0.1'
    ):
        """Basic robot framework command line tools.

        :param source: robot files, can be one or a folder.
        :type source: string.
        :param output: robot -d/--outputdir.
        :type output: string.
        """
        self.prog = prog
        self.description = description
        self.epilog = epilog
        self.version = version

        self.suite = Suite(sources=BaseUtils.expandpath(source))
        self.outputdir = BaseUtils.expandpath(output)

        self.args = None

    def __define_options(self):
        self.parser = argparse.ArgumentParser(
            prog=self.prog,
            description=self.description,
            epilog=self.epilog,
            add_help=True
        )
        self.basic_parser = self.parser.add_argument_group(
            "Test Case Options."
        )
        self.basic_parser.add_argument(
            '-D', '--debug',
            action='store_true',
            required=False,
            help='Debug mode.',
            dest='debug'
        )
        self.basic_parser.add_argument(
            '-V', '--version',
            action='version',
            version='%(prog)s {}'.format(self.version)
        )
        self.basic_parser.add_argument(
            '-P', '--pythonpath',
            required=False,
            help='Specify PYTHONPATH for develop package.',
            dest='pythonpath'
        )

    def __define_sub_options(self):
        self.subparsers = self.parser.add_subparsers(
            title="Workflow Options.",
            dest='option',
            description='sub options for worklfows',
            help='specify the workflow option.'
        )

        self.run_parser = self.subparsers.add_parser(
            'run',
            help='run workflows.',
            description='options for run workflows.'
        )
        self.run_parser.add_argument(
            '-a', '--all',
            action='store_const',
            const=self.suite.workflowlist,
            help='Run all workflows.'
        )
        self.run_parser.add_argument(
            '-s', '--specify',
            nargs='+',
            default=[],
            help='Run specify workflow by index.',
            dest='specify'
        )
        self.run_parser.add_argument(
            '-t', '--test',
            nargs='+',
            default=[],
            help='Run specify workflow by workflow/case name.',
            dest='test'
        )
        self.run_parser.add_argument(
            '-i', '--include',
            nargs='+',
            default=[],
            help='Run specify workflow by workflow/case tags.',
            dest='include'
        )
        self.run_parser.add_argument(
            '-e', '--exclude',
            nargs='+',
            default=[],
            help='Ignore specify workflow by workflow/case tags.',
            dest='exclude'
        )

        self.show_parser = self.subparsers.add_parser(
            'show',
            help='show workflows.',
            description='options for show workflows.'
        )
        self.show_parser.add_argument(
            '-a', '--all',
            action='store_const',
            const=self.suite.workflowlist,
            help='List all workflows.'
        )
        self.show_parser.add_argument(
            '-d', '--detail',
            nargs='+',
            help='Show details for specify workflow by index.',
            dest='detail'
        )

    def __parse_run(self):
        if self.args.all or \
                self.args.specify or \
                self.args.test or \
                self.args.include or \
                self.args.exclude:
            index_list = []
            test_list = []
            include_list = []

            if self.args.specify:
                index_list = [
                    self.suite.get_workflow_name_by_index(index)
                    for index in self.args.specify
                ]
            if self.args.test:
                test_list = self.suite.get_workflow_by_name(self.args.test)
            if self.args.include:
                include_list = self.suite.get_workflows_by_tags(
                    self.args.include)
            workflows_list = index_list + test_list + include_list
            # if specify nothing, use default
            workflows_list = workflows_list if workflows_list else \
                self.suite.workflowlist
            # remove exclude
            if self.args.exclude:
                workflows_list = self.suite.remove_workflow_by_tags(
                    workflows_list, self.args.exclude
                )
            # remove 'disabled' tag workflow
            _disabled_tag = 'DISABLED'
            if self.suite.get_workflows_by_tags([_disabled_tag]):
                workflows_list = self.suite.remove_workflow_by_tags(
                    workflows_list, [_disabled_tag]
                )
                print(
                    BaseColor.BLUE(
                        '\nworkflow with "{}" tag are excluded by '
                        'default\n'.format(_disabled_tag)
                    )
                )

            if workflows_list:
                return self.__robot_run(workflows_list)
            else:
                print(
                    BaseColor.YELLOW(
                        "No workflow has been specified to run."
                    )
                )
                return -1
        else:
            print(
                BaseColor.RED(
                    "Usage ERROR"
                )
            )
            return -1

    def __parse_show(self):
        if self.args.all:
            header = ['ID', 'TAGS', 'TITLE']
            formatter = ['{0:<5}', '{1:<30}', '{2}']
            partial_func = [BaseColor.MAGENTA, BaseColor.CYAN, BaseColor.GREEN]

            format_wf = ''.join(formatter)
            print(format_wf.format(*header))
            print(format_wf.format(
                *(
                    '=' * len(col)
                    for col in header
                )
            ))
            format_wf = ''
            for func, param in zip(partial_func, formatter):
                format_wf += func(param)

            print('\n'.join(
                format_wf.format(
                    index,
                    [str(tag) for tag in workflow.tags],
                    workflow.name
                ) for index, workflow in enumerate(
                    self.suite.workflowdict.values(), 1
                )
            ))
        if self.args.detail:
            print('')
            for index in self.args.detail:
                name = self.suite.get_workflow_name_by_index(index)
                if name in self.suite.workflowdict:
                    workflow = self.suite.workflowdict[name]
                    help = HelpFormatter('')
                    help.start_section(
                        BaseColor.GREEN(
                            '{}'.format(
                                workflow.name[0]
                            )
                        )
                    )
                    help.add_text(workflow.doc[0])
                    help.start_section('TAGS')
                    help.add_text(str([str(tag) for tag in workflow.tags]))
                    help.start_section('AUC STEPS')
                    for key in workflow.keywords:
                        help.add_argument(
                            Action('', '', help=BaseColor.BLUE(key))
                        )
                    help.end_section()
                    help.end_section()
                    help.end_section()
                    print(help.format_help())
        return 0

    def __robot_run(self, workflows):
        __options = {}
        __timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        __outputdir = os.path.join(
            self.outputdir, 'outputdir_' + __timestamp
        )
        if not os.path.exists(__outputdir):
            os.makedirs(__outputdir, 0755)
        __summary_path = os.path.join(
            __outputdir, 'summary_' + __timestamp + '.txt'
        )

        logger.info("outputdir: {}".format(__outputdir), also_console=True)

        if self.args.pythonpath:
            print("my pythonpath: ", self.args.pythonpath)
            __options.setdefault('pythonpath', self.args.pythonpath)

        if not self.args.debug:
            # If not debug mode, don't print TRACE/DEBUG/INFO/WARN to log.
            __options.setdefault('loglevel', 'ERROR')
            # And print debug message to debug file.
            __options.setdefault('debugfile', 'debug.log')
        else:
            # If debug mode, print everything to log file.
            __options.setdefault('loglevel', 'DEBUG:INFO')

        with Output(__summary_path) as output:
            robot.run(
                *self.suite.test_files,
                outputdir=__outputdir,
                timestampoutputs=False,
                test=workflows,
                consolecolors='on',
                consolewidth=79,
                consolemarkers='on',
                stdout=output,
                **__options
            )

        output_file = os.path.join(
            __outputdir, "output.xml"
        )
        result = ExecutionResult(output_file)
        result.configure(stat_config={
            "suite_stat_level": 2,
            "tag_stat_combine": "tagANDanother"}
        )
        return result.return_code

    def parse_options(self):
        try:
            self.__define_options()
            self.__define_sub_options()
            self.args = self.parser.parse_args()

            if self.args.option == 'run':
                return self.__parse_run()
            elif self.args.option == 'show':
                return self.__parse_show()
        except Exception:
            raise
