"""
This script provides tests for 'whatprovides' project

Author:
 shmakovpn <shmakovpn@yandex.ru>

Date:
 2020-06-21
"""
import os
import sys
import re
import unittest
from typing import Pattern, List
from .whatprovides import DeclarationType, declaration_types, Declaration, filter_declaration, \
    ifilter_declaration, re_filter_declaration, FileLine, get_declarations, get_files_lines, get_python_files, \
    get_paths, filter_delaration_type


SCRIPT_PATH: str = os.path.dirname(os.path.abspath(__file__))
TEST_STRING_IO: bool = False


class TestWhatprovides(unittest.TestCase):
    def setUp(self) -> None:
        self.test_path: str = os.path.join(os.path.dirname(SCRIPT_PATH), 'test')

    def test_declaration_type_init(self):
        try:
            declaration_types.append(
                DeclarationType(
                    name='wrong_pattern',
                    pattern=re.compile(r'^pattern without the "name" group')
                )
            )
            self.assertTrue(False, f"Checking for wrong pattern failed")
        except RuntimeError as e:
            pass
        else:
            self.assertTrue(False, f"Checker for wrong pattern doe not work! '{e}' was not caught")
        line_var: str = 'some_var = "some value"'
        self.assertEqual(declaration_types[0].search(line=line_var), 'some_var')

    def test_declaration_type_search(self):
        line_var: str = 'variable_name = "variable value"'
        variable_name: str = declaration_types[0].search(line=line_var)
        self.assertEqual(variable_name, 'variable_name')
        line_def: str = 'def function_name(*args, **kwargs):'
        function_name: str = declaration_types[1].search(line=line_def)
        self.assertEqual(function_name, 'function_name')
        line_class: str = 'class ClassName(ParentClass):'
        class_name: str = declaration_types[2].search(line=line_class)
        self.assertEqual(class_name, 'ClassName')

    def test_filter_declaration(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[0], name='not_filtered', module_path=''),
        ]
        filtered_declarations: List[Declaration] = list(
            filter_declaration(search='not', declarations=declarations)
        )
        self.assertEqual(len(filtered_declarations), 1)
        self.assertEqual(filtered_declarations[0].name, 'not_filtered')

    def test_ifilter_declaration(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[0], name='NOT_filtered', module_path=''),
        ]
        filtered_declarations: List[Declaration] = list(
            ifilter_declaration(search='Not', declarations=declarations)
        )
        self.assertEqual(len(filtered_declarations), 1)
        self.assertEqual(filtered_declarations[0].name, 'NOT_filtered')

    def test_re_filter_declaration(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[0], name='not_filtered_123', module_path=''),
        ]
        filter_declarations: List[Declaration] = list(
            re_filter_declaration(search=re.compile(r'not_[a-zA-Z0-9_]+'), declarations=declarations)
        )
        self.assertEqual(len(filter_declarations), 1)
        self.assertEqual(filter_declarations[0].name, 'not_filtered_123')

    def test_get_declarations(self):
        lines: List[FileLine] = [
            FileLine(file_path='', line_number=1, line='# some comment'),
            FileLine(file_path='', line_number=1, line='variable = "value"'),
            FileLine(file_path='', line_number=1, line='def some_function(*args, **kwargs):'),
            FileLine(file_path='', line_number=1, line='class SomeClass(ParentClass):'),
            FileLine(file_path='', line_number=1, line='x==1'),
            FileLine(file_path='', line_number=1, line='# def filtered_function():'),
            FileLine(file_path='', line_number=1, line='    class Meta:'),
        ]
        declarations: List[Declaration] = list(
            get_declarations(lines=lines)
        )
        self.assertEqual(len(declarations), 3)
        self.assertEqual(declarations[0].name, 'variable')
        self.assertEqual(declarations[0].declaration_type, declaration_types[0])
        self.assertEqual(declarations[1].name, 'some_function')
        self.assertEqual(declarations[1].declaration_type, declaration_types[1])
        self.assertEqual(declarations[2].name, 'SomeClass')
        self.assertEqual(declarations[2].declaration_type, declaration_types[2])

    def test_get_files_lines(self):
        file_paths: List[str] = [
            os.path.join(self.test_path, 'test_data1.py'),
            os.path.join(self.test_path, 'test_data2.py'),
            os.path.join(self.test_path, 'ja.py')
        ]
        file_lines: List[FileLine] = list(
            get_files_lines(file_paths=file_paths)
        )
        self.assertEqual(len(file_lines), 68)
        self.assertEqual(file_lines[0].line_number, 0)
        self.assertEqual(file_lines[0].file_path, file_paths[0])
        self.assertEqual(file_lines[0].line, "variable1 = 'value1'\n")

    def test_get_python_files(self):
        file_paths: List[str] = list(
            get_python_files([self.test_path])
        )
        sub_folder_path: str = os.path.join(self.test_path, 'sub_folder')
        sub_sub_folder_path: str = os.path.join(sub_folder_path, 'sub_sub_folder')
        sub_folder2_path: str = os.path.join(self.test_path, 'sub_folder2')
        sub_sub_folder2_path: str = os.path.join(sub_folder2_path, 'sub_sub_folder2')
        self.assertIn(os.path.join(sub_folder_path, 'sub_folder_item.py'), file_paths)
        self.assertIn(os.path.join(sub_sub_folder_path, 'sub_sub_folder_item.py'), file_paths)
        self.assertIn(os.path.join(sub_sub_folder2_path, 'sub_sub_folder2_item.py'), file_paths)
        self.assertNotIn(os.path.join(sub_folder_path, 'not_item.txt'), file_paths)

    def test_get_paths(self):
        paths: List[str] = [
            os.path.join(self.test_path, 'sub_folder'),
            os.path.join(self.test_path, 'sub_folder2'),
            os.path.join(self.test_path, 'not_folder.txt'),
        ]
        python_paths: List[str] = list(
            get_paths(paths)
        )
        self.assertEqual(len(python_paths), 2)
        self.assertEqual(python_paths[0], paths[0])
        self.assertEqual(python_paths[1], paths[1])

    def test_declaration_types_in(self):
        some_type: DeclarationType = declaration_types[1]
        self.assertIn(some_type, declaration_types)

    def test_filter_declaration_type(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[1], name='not_filtered_123', module_path=''),
        ]
        filtered: List[Declaration] = list(
            filter_delaration_type(declarations=declarations, remained_types=[declaration_types[1]])
        )
        self.assertEqual(len(filtered), 1)

    def test_string_io(self):
        if TEST_STRING_IO:
            results = re_filter_declaration(
                re.compile('^StringIO$'),
                get_declarations(get_files_lines(get_python_files(get_paths(sys.path))))
            )
            class_results = filter_delaration_type(results, [declaration_types[2]])
            self.assertTrue(any(class_results))

