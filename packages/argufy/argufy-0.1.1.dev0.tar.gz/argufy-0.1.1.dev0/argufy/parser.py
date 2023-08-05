# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Argufier is an inspection based CLI parser.'''

import inspect
from argparse import ArgumentParser
from types import ModuleType
from typing import Any, Callable, Optional, Sequence, Type, TypeVar

# from argparse_color_formatter import ColorHelpFormatter, ColorTextWrapper
from docstring_parser import parse

# from .__version__ import __version__
from .argument import Argument

F = TypeVar('F', bound=Callable[..., Any])


class Parser(ArgumentParser):
    '''Provide CLI parser for function.'''

    def __init__(self, *args: str, **kwargs: str) -> None:
        '''Initialize parser.

        Parameters
        ----------
        prog: str
            The name of the program
        usage: str
            The string describing the program usage
        description: str
            Text to display before the argument help
        epilog: str
            Text to display after the argument help
        parents: list
            A list of ArgumentParser objects whose arguments should also
            be included
        formatter_class: Object
            A class for customizing the help output
        prefix_chars: char
            The set of characters that prefix optional arguments
        fromfile_prefix_chars: None
            The set of characters that prefix files from which additional
            arguments should be read
        argument_default: None
            The global default value for arguments
        conflict_handler: Object
            The strategy for resolving conflicting optionals
        add_help: str
            Add a -h/--help option to the parser
        allow_abbrev: bool
            Allows long options to be abbreviated if the abbreviation is
            unambiguous

        '''
        # self.__log = Logger(__name__)
        # self.__log.info("Loading command line tool settings")
        super().__init__(*args, **kwargs)  # type: ignore

    def add_arguments(
        self, fn: F, parser: Optional[Type[ArgumentParser]] = None
    ) -> None:
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self  # type: ignore
        signature = inspect.signature(fn)
        docstring = parse(fn.__doc__)
        for arg in signature.parameters:
            description = next(
                (d for d in docstring.params if d.arg_name == arg), None
            )
            argument = Argument(
                signature.parameters[arg], description  # type: ignore
            )
            name = argument.attributes.pop('name')
            parser.add_argument(*name, **argument.attributes)  # type: ignore

    def add_subcommands(
        self, module: ModuleType, exclude_prefix: str = '_'
    ) -> None:
        '''Add subparsers.'''
        subparsers = self.add_subparsers()
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            if fn.__module__ == module.__name__ and not name.startswith(
                exclude_prefix
            ):
                help = parse(fn.__doc__).short_description
                subparser = subparsers.add_parser(name, help=help)
                subparser.set_defaults(fn=fn)
                self.add_arguments(fn, subparser)  # type: ignore

    def dispatch(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[str] = None,
    ) -> Callable[[F], F]:
        '''Call command with arguments.'''
        result = self.parse_args(args, namespace)
        fn = vars(result).pop('fn')
        return fn(**vars(result))
