import argparse

from .utils import Suite


class BaseRF(object):

    def __init__(self):


    def __define_options(
            self,
            prog='super-devops',
            description='robot framework command customize.',
            epilog='robot framework command options',
            add_help=True
    ):
        self.parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            epilog=epilog,
            add_help=add_help
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
            version='%(prog)s 0.0.1'
        )

    def _define_sub_options(self):
        self.subparsers = self.parser.add_subparsers(
            title="Workflow Options.",
            description='',
            dest='option',
            help=''
        )

        self.run_parser = self.subparsers.add_parser(
            'run', help='run workflows.',
            description='options for run workflows.'
        )
        self.workflow_parser.add_argument()

        self.show_parser = self.subparsers.add_parser(
            'show',
            help='show workflows.',
            description='options for show workflows.'
        )
        self.show_parser.add_argument()

    def _parse_options(self):
        try:
            self.args = self.parser_args()
        except Exception:
            raise
