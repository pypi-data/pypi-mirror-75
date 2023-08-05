from prompy.ProMExecutor import ProMExecutor

from pathlib import Path
import zipfile
import os
import re


class FunctionVariant:
  def __init__(self, argument_classes, return_classes):
    self.argument_classes = [class_name for class_name in argument_classes if class_name != '']
    self.return_classes = [class_name for class_name in return_classes if class_name != '']

class Function:
  def __init__(self, function_name, argument_classes, return_classes):
    self.function_name = function_name
    self.variants = [FunctionVariant(argument_classes, return_classes)]

  def add_variant(self, argument_classes, return_classes):
    self.variants.append(FunctionVariant(argument_classes, return_classes))

  def __str__(self):
    return f'{self.function_name} -> \n' + '\n'.join([str(variant) for variant in self.variants])

class DocumentationReader:
  def __init__(self, parameters):
    self.parameters = parameters
    self.prom_directory = parameters['prom_directory']
    self.lib_directory  = parameters['lib_directory']
    self.dist_directory = parameters['dist_directory']
    self.functions = {}
    self.classes = set()

  def __fix_class_name(self, class_name):
    if class_name[-2:] == '[]':
      return class_name[:-2] + 'List'
    return class_name

  def parse_plugin(self, plugin_text):
    function_name    = plugin_text.split('(')[0]
    argument_classes = [self.__fix_class_name(class_name) for class_name in plugin_text.split('(')[1].split(')')[0].split(', ')]
    return_classes   = [self.__fix_class_name(class_name) for class_name in plugin_text.split('>')[1].strip(' ()').split(', ')]
    return function_name, argument_classes, return_classes

  def read_all_plugins(self):
    prom_executor = ProMExecutor(self.parameters)
    functions = prom_executor.get_available_functions()

    for function in functions:
      if '->' not in function:
        continue
      function = function.rstrip('\r\n')
      function_name, argument_classes, return_classes = self.parse_plugin(function)
      self.classes.update(argument_classes)
      self.classes.update(return_classes)
      if function_name not in self.functions:
        self.functions[function_name] = Function(function_name, argument_classes, return_classes)
      else:
        self.functions[function_name].add_variant(argument_classes, return_classes)


class DocumentationGenerator:
  def __init__(self, document_file):
    self.document_file = document_file

  def __create_function_definition_string(self, function_name, argument_classes, return_classes, tabs=0):
    prefix = ' ' * 4 * tabs
    arguments = []
    for index, class_name in enumerate(argument_classes):
      repetitions = argument_classes[:index].count(class_name)
      arguments.append(f'f{class_name}{"" if repetitions == 0 else repetitions}: {class_name}')
    arguments = ', '.join(arguments)

    returns = f'{", ".join(return_classes)}' if len(return_classes) == 1 else f'({", ".join(return_classes)})'
    function_string = f'{prefix}def {function_name}({arguments}) -> {returns}:\n'

    # TODO check no returns
    function_string += f'{prefix}    return {", ".join([c + "()" for c in return_classes])}'
    return function_string + '\n'

  def create_function_definition_string(self, function):
    if len(function.variants) == 1:
      variant = function.variants[0]
      definition_string = self.__create_function_definition_string(function.function_name, variant.argument_classes, variant.return_classes)
      return definition_string
    else:
      return_classes = function.variants[0].return_classes
      returns = f'{", ".join(return_classes)}' if len(return_classes) == 1 else f'({", ".join(return_classes)})'
      definition_string = f'def {function.function_name}(*args) -> {returns}:\n'
      for index, variant in enumerate(function.variants):
        definition_string += self.__create_function_definition_string(f'f{index}', variant.argument_classes, variant.return_classes, tabs=1)
      fs = [f'f{index}' for index in range(len(function.variants))]
      definition_string += f'    d = next((d for d in [{", ".join(fs)}] if check_arguments(d, args)), None)\n'
      definition_string +=  '    return d(*args)\n'
      return definition_string

  def generate(self, classes, functions):
    header = 'from prompy.utils import check_arguments'

    body = header + '\n\n'
    for class_name in classes:
      if class_name != '':
        body += f'class {class_name}:\n    def __init__(self, *args): pass\n'
    body += '\n\n'

    for function in functions.values():
      body += self.create_function_definition_string(function) + '\n\n'

    with open(self.document_file, 'w') as document_file:
      document_file.write(body)


def generate_documentation(filename, parameters):
  documentationReader = DocumentationReader(parameters)
  documentationReader.read_all_plugins()

  generator = DocumentationGenerator(Path(filename))
  generator.generate(documentationReader.classes, documentationReader.functions)
