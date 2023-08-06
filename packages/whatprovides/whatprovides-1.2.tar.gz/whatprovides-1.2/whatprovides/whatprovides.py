"""
This script provides search for an importing path of a module in the
*PYTHON PATH* of the currently activated virtual environment.

In used idea, it is a some analog of *whatprovides* command of *yum* package manager,
but works with python modules instead of packages.

Author:
 shmakovpn <shmakovpn@yandex.ru>

Date:
 2020-06-21
"""
import os
import sys
import re
import argparse
from chardet.universaldetector import UniversalDetector
from typing import List, Pattern, Match, Iterator
from functools import partial


class DeclarationType:
    """
    Python declaration type

    Declaration type can be one of this:
     - var: some_variable = some_value
     - def: def some_func(arg, ):
     - class: class SomeClass(SomeParent):

    :param name: a name of a declaration (var, def, class)
    :type name: str
    :param pattern: a pattern to match a declaration in a string
    :type pattern: Pattern
    """

    def __init__(self, name: str, pattern: Pattern):
        self.name = name
        if 'name' not in pattern.groupindex:
            raise RuntimeError(
                '"%s.__init__" pattern "%s" does not contains the "name" group' % (
                    self.__class__.__name__,
                    pattern,
                )
            )
        self.pattern = pattern

    def search(self, line: str) -> str:
        """
        Search in a *line* using *self.pattern*, returns the *name* matching group or an empty string,
        if search was failed

        :param line: a line to search
        :type line: str
        :return: the *name* matching group or an empty string if search was failed
        :rtype str:
        :raises KeyError: This exception raises if search result does not contains the 'name' group
        """
        match: Match = self.pattern.search(line)
        if not match:
            return ''  # returns an empty string if search was failed
        return match.group('name')


#: types of declaration used in python code (e.g. variables, function, classes)
declaration_types: List[DeclarationType] = [
    DeclarationType(
        name='var',
        pattern=re.compile(r'^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+=[^=]'),
    ),
    DeclarationType(
        name='def',
        pattern=re.compile(r'^def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[\s(]'),
    ),
    DeclarationType(
        name='class',
        pattern=re.compile(r'^class\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[\s:(]'),
    ),
]


class Declaration:
    """
    Declaration of a name in python

    :param declaration_type: a type of a declaration (variable, def, class ...)
    :type declaration_type: DeclarationType
    :param name: a name of a variable or a function or a class
    :type name: str
    :param module_path: a path to python_module where the declaration was found
    :type module_path: str
    """

    def __init__(self, declaration_type: DeclarationType, name: str, module_path: str):
        self.declaration_type = declaration_type
        self.name = name
        self.module_path = module_path

    def __str__(self) -> str:
        return '%s: %s: %s' % (self.declaration_type.name, self.name, self.module_path)


def filter_declaration(search: str, declarations: Iterator[Declaration], ) -> Iterator[Declaration]:
    """
    This generator will filter declarations by name of declaration
    case sensitive

    :param search: A part of a name for case sensitive search
    :type search: str
    :param declarations: An iterable of declarations
    :type declarations: Iterator[Declaration]
    :return: generator of filtered declarations
    :rtype: Iterator[Declaration]
    """
    for declaration in declarations:
        if search in declaration.name:
            yield declaration


def ifilter_declaration(search: str, declarations: Iterator[Declaration], ) -> Iterator[Declaration]:
    """
    This generator will filter declarations by name of declaration
    case insensitive
    :param search: A part of a name of case insensitive search
    :type search: str
    :param declarations: An iterable of declarations
    :type declarations: Iterator[Declaration]
    :return: generator of filtered declarations
    :rtype: Iterator[Declaration]
    """
    search_lower: str = search.lower()
    for declaration in declarations:
        if search_lower in declaration.name.lower():
            yield declaration


def re_filter_declaration(search: Pattern, declarations: Iterator[Declaration], ) -> Iterator[Declaration]:
    """
    This generator will filter declarations by name if declaration
    using the compiled regular expression
    :param search: a pattern to match name of declaration
    :type search: Pattern
    :param declarations: An iterable of declarations
    :type declarations: Iterator[Declaration]
    :return: generator of filtered declarations
    :rtype: Iterator[Declaration]
    """
    for declaration in declarations:
        if search.search(declaration.name):
            yield declaration


class FileLine:
    """
    A line of a file

    :param file_path: A path to a file contains this line
    :type file_path: str
    :param line_number: A number of this line
    :type line_number: int
    :param line: a content of this line
    :type line: str
    """

    def __init__(self, file_path: str, line_number: int, line: str):
        self.file_path: str = file_path
        self.line_number: int = line_number
        self.line: str = line

    def __str__(self):
        return '%i: %s: %s' % (self.line_number, self.file_path, self.line.rstrip())


def get_declarations(lines: Iterator[FileLine]) -> Iterator[Declaration]:
    """
    This generator creates instances of declaration
    from lines of code which contains declaration of variables or functions or classes

    :param lines: an iterable of lines of code
    :type lines: Iterator[FileLine]
    :return: a generator of instances of declaration
    :rtype: Iterator[Declaration]
    """
    for line in lines:
        for declaration_type in declaration_types:
            declaration_name: str = declaration_type.search(line=line.line)
            if declaration_name:
                yield Declaration(
                    declaration_type=declaration_type,
                    name=declaration_name,
                    module_path=line.file_path,
                )
                break


def get_file_lines(file_paths: Iterator[str]) -> Iterator[FileLine]:
    """
    This generator creates instances of a line of a file
    from paths to files

    :param file_paths: An iterable of file paths
    :type file_paths: Iterator[str]
    :return: a generator of instances of lines of files
    :rtype: Iterator[FileLine]
    """
    for file_path in file_paths:
        line_number: int = 0
        with open(file_path, 'rb') as file:
            for line in file:
                detector: UniversalDetector = UniversalDetector()
                detector.feed(line)
                yield FileLine(
                    file_path=file_path,
                    line_number=line_number,
                    line=line.decode(detector.result.get('encoding') or sys.getdefaultencoding()),
                )
                detector.reset()
                line_number += 1
        # try:
        #     with open(file_path, 'r') as file:  # try to read a file using default encoding
        #         for line in file:
        #             yield FileLine(
        #                 file_path=file_path,
        #                 line_number=line_number,
        #                 line=line,
        #             )
        #             line_number += 1
        # except UnicodeDecodeError as unicode_decode_error:
        #     with open(file_path, 'r', encoding='utf-8') as file:  # read file using utf-8 encoding
        #         for line in file:
        #             yield FileLine(
        #                 file_path=file_path,
        #                 line_number=line_number,
        #                 line=line,
        #             )
        #             line_number += 1


def get_python_files(search_paths: Iterator[str]) -> Iterator[str]:
    """
    This generator yields paths of python files from search paths

    :param search_paths: An iterable of search paths
    :type search_paths: Iterator[str]
    :return: a generator of paths of python files
    :rtype: Iterator[str]
    """
    for search_path in search_paths:
        for item in os.listdir(search_path):
            if item.lower() == '__pychache__':
                continue
            item_path: str = os.path.join(search_path, item)
            if os.path.isfile(item_path):
                if item.lower().endswith('.py'):
                    yield item_path
            elif os.path.isdir(item_path):
                for sub_item_path in get_python_files([item_path]):
                    yield sub_item_path


def get_paths(paths: Iterator[str]) -> Iterator[str]:
    """
    This generator filters an iterable of paths,
    remaining only python libraries folders paths

    :param paths: An iterable of paths
    :type paths: Iterator[str]
    :return: a generator of paths of python libraries folders
    :rtype: Iterator[str]
    """
    for path in paths:
        if os.path.isdir(path):
            yield path


def filter_delaration_type(
        declarations: Iterator[Declaration],
        remained_types: List[DeclarationType],
) -> Iterator[Declaration]:
    """
    This generator filters instances of Declaration by a list of declaration types

    :param declarations: an iterable of Declarations to filter
    :type declarations: Iterator[Declarations]
    :param remained_types: only declarations of type from this list will remain.
    :type remained_types: List[DeclarationType]
    :return: filtered declarations
    :rtype: Iterator[Declarations]
    """
    for declaration in declarations:
        if declaration.declaration_type in remained_types:
            yield declaration


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-r', help='enables search using a regex pattern', action='store_true')
    parser.add_argument('-i', help='ignore case', action='store_true')
    parser.add_argument('search', help='a regex pattern (if using -r) or string to search for')
    parser.add_argument('-v', help='show only variables, this option can be combined with the -c or -d options',
                        action='store_true')
    parser.add_argument('-c', help='show only classes, this option can be combined with the -v or -d options',
                        action='store_true')
    parser.add_argument('-d', help='show only functions, this option can be combined with the -v or -c options',
                        action='store_true')
    args: argparse.Namespace = parser.parse_args()
    if args.r and args.i:
        _filter: partial = partial(re_filter_declaration, re.compile(args.search, re.IGNORECASE))
    elif args.r:
        _filter: partial = partial(re_filter_declaration, re.compile(args.search))
    elif args.i:
        _filter: partial = partial(ifilter_declaration, args.search)
    else:
        _filter: partial = partial(filter_declaration, args.search)
    results: Iterator[Declaration] = _filter(
        declarations=get_declarations(
            lines=get_file_lines(
                file_paths=get_python_files(
                    search_paths=get_paths(sys.path)
                )
            )
        )
    )
    if not args.v and not args.d and not args.c:
        filtered_results: Iterator[Declaration] = results
    elif args.v and args.d and args.c:
        filtered_results: Iterator[Declaration] = results
    else:
        remained_types: List[DeclarationType] = []
        if args.v:
            remained_types.append(declaration_types[0])
        if args.d:
            remained_types.append(declaration_types[1])
        if args.c:
            remained_types.append(declaration_types[2])
        filtered_results: Iterator[Declaration] = filter_delaration_type(results, remained_types=remained_types)
    for result in filtered_results:
        print(result)


if __name__ == '__main__':
    main()
