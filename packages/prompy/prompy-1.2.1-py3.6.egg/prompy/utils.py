import inspect

def check_arguments(function, arguments):
  parameters = list(inspect.signature(function).parameters.values())
  if len(parameters) != len(arguments):
    return False
  for parameter, argument in zip(parameters, arguments):
    if parameter.annotation != type(argument):
      return False
  return True

