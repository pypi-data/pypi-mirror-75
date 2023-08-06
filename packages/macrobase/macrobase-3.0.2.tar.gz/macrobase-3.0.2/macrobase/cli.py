import argparse
import sys
from typing import List

from macrobase.app import Application
from macrobase.hook import HookNames


class Cli:

    def __init__(self, app: Application, program: str = 'macrobase', description: str = None):
        self._app = app
        self._parser = argparse.ArgumentParser(prog=program, description=description)
        self._subparsers = self._parser.add_subparsers(dest='catalog')

        self._add_start_command()
        self._add_hooks_command()

    def _add_start_command(self):
        # start command
        start_parser = self._subparsers.add_parser('start', help='start drivers')
        start_parser.description = 'Start drivers by names.'

        start_parser.add_argument(
            'drivers',
            nargs='?',
            type=str,
            help='Choose drivers names',
        )
        start_parser.add_argument('-a', '--all', action='store_true', default=False, help='start all drivers')

    def _add_hooks_command(self):
        hooks_parser = self._subparsers.add_parser('hooks', help='hook management')
        hooks_parser.description = 'Manager application hooks'

        # start hooks command
        start_parser = hooks_parser.add_subparsers(dest='action').add_parser('run', help='run hooks')

        start_parser.add_argument(
            'hook_name',
            choices=[h.value for h in HookNames],
            help='Choose hook names',
        )
        # hooks_parser.add_argument('-a', '--all', action='store_true', default=False, help='start all hooks')

    def execute(self):
        try:
            parsed_args = self._parser.parse_args()
            self._execute(parsed_args)
        except SystemExit:
            return

    def _execute(self, parsed_args: argparse.Namespace):
        if parsed_args.catalog == 'start':
            self._execute_start(parsed_args)
        elif parsed_args.catalog == 'hooks':
            self._execute_hooks(parsed_args)
        else:
            print('unknown command')
            sys.exit(0)

    def _get_application_drivers_aliases(self) -> List[str]:
        return list(self._app.drivers.keys())

    def _execute_start(self, parsed_args: argparse.Namespace):
        drivers = []
        if parsed_args.drivers is not None:
            drivers = parsed_args.drivers.split(',')

            # validate drivers
            unexpected_drivers = list(filter(lambda d: d not in self._get_application_drivers_aliases(), drivers))
            if len(unexpected_drivers) > 0:
                self._parser.error(f"Unexpected drivers `{','.join(unexpected_drivers)}`")

        if parsed_args.all and len(drivers) > 0:
            print('warning: using `--all` argument with any drivers will cause run all drivers.')

        if parsed_args.all:
            self._app.run()
        else:
            self._app.run(aliases=parsed_args.drivers)

    def _execute_hooks(self, parsed_args: argparse.Namespace):
        hook = HookNames(parsed_args.hook_name)
        self._app.call_hooks(hook)
