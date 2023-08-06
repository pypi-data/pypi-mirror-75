from inspect import ismodule, isfunction, signature, Parameter
from importlib import import_module
from sys import modules
from os.path import exists, join
from os import getcwd
import logging


def __get_cur_module():
    return modules[globals()['__name__']]


def __get_module(module_name, package_path):
    if (isinstance(module_name, str) and exists(join(package_path, module_name + '.py'))) and isinstance(package_path, str):
        return import_module(name=module_name, package=package_path)

    elif not isinstance(module_name, str):
        raise ValueError('Need to specify the module name!')

    elif not isinstance(package_path, str):
        raise ValueError('Need to specify the path to the module!')

    elif not exists(join(package_path, module_name + '.py')):
        raise ValueError('Package path {0} does not exist!'.format(join(package_path, module_name + '.py')))


def __get_function(module, func_name):
    if ismodule(module) and isinstance(func_name, str):
        return getattr(module, func_name)
    else:
        raise ValueError('Need to specify the function name!')


def __subset_dictionary(dict_, subset_keys):
    if isinstance(dict_, dict) and (isinstance(subset_keys, list) or isinstance(subset_keys, set)):
        return {key: value for key, value in dict_.items() if key in subset_keys}

    elif not isinstance(dict_, dict):
        TypeError('{0} invalid type for <dict_>!'.format(type(dict_)))

    else:
        TypeError('{0} is not supported for subset keys; use either a list or a set!'.format(type(subset_keys)))


def get_required_params(func):
    """
    Return a set of params in <func>'s header that don't have default values

    :param func: Function Object
    :return: Set of String in <func> that don't have default values

    >>> get_required_params(gexec).difference({'params', 'func'})
    set()
    """

    if isfunction(func):
        return set([key for key, default_value in signature(func).parameters.items() if default_value.default is Parameter.empty])
    else:
        raise TypeError('{0} invalid type! Need a function object!'.format(type(func)))


def get_optional_params(func):
    """
    Return a set of params in <func>'s header that have default values

    :param func: Function Object
    :return: Set of String in <func> that have default values

    >>> get_optional_params(gexec).difference({'module', 'package_path'})
    set()
    """

    if isfunction(func):
        return set([key for key, default_value in signature(func).params.items() if default_value.default is not Parameter.empty])
    else:
        raise TypeError('{0} invalid type! Need a function object!'.format(type(func)))


def __get_valid_input(func, params):
    if not isfunction(func):
        TypeError('{0} not supported! Need a function object!'.format(type(func)))
    elif not isinstance(params, dict):
        TypeError('{0} not supported! Params needs to be a dictionary!'.format(type(params)))

    parameter_keys = set(params.keys())

    required_params = get_required_params(func)

    if bool(required_params - parameter_keys):
        raise ValueError('Missing params:\n{0}'.format(', '.join(required_params - parameter_keys)))

    all_func_keys = set(signature(func).parameters.keys())

    valid_parameter_keys = parameter_keys.intersection(all_func_keys)

    valid_params = __subset_dictionary(params, valid_parameter_keys)

    return valid_params


def __get_module_obj(module, package_path):
    if not isinstance(module, str):
        raise TypeError('module must be either a Module Object or a String!')

    elif not isinstance(package_path, str):
        raise ValueError('Need to set a valid package_path when <module> is a string!')

    elif not exists(package_path):
        raise ValueError('Invalid package path: "{0}"'.format(package_path))

    elif not exists(join(package_path, module + '.py')):
        raise ValueError('Module "{0}" does not exist at "{1}"!'.format(module, package_path))

    else:
        module = __get_module(module_name=module, package_path=package_path)

    return module


def __get_function_obj(func, module=None, package_path=None):
    if isinstance(func, str):
        if not ismodule(module):
            # <module> is not a Module Object

            if isinstance(package_path, str):
                module = __get_module_obj(module=module, package_path=package_path)

            elif hasattr(__get_cur_module(), func):
                module = __get_cur_module()

            else:
                raise ValueError('If the function is not in the current module, package_path must specify the directory!')

        func = __get_function(module=module, func_name=func)

    else:
        raise TypeError('{0} type not supported! <func> must be either a Function Object or a String!'.format(type(func)))

    return func


def gexec(func, params, module=None, package_path=None):
    """
    Executes the function <func> using the intersection of params between the
        function header and keys in <params>

    Note:
        If the func is a String and is not in the current module;
            it will try to import the module <module> in <package_path> to execute <func>

    :param func: Function Object | String
    :param params: Dictionary
    :param module: Module Object | String
    :param package_path: String
    :return: None | Object

    >>> gexec(func=__subset_dictionary, params={'dict_': {'a': 1, 'b': 2}, 'subset_keys': {'a'}})
    {'a': 1}

    >>> gexec(func='__subset_dictionary', params={'dict_': {'a': 1, 'b': 2}, 'subset_keys': {'a'}})
    {'a': 1}

    >>> gexec(func='__subset_dictionary', params={'dict_': {'a': 1, 'b': 2}, 'subset_keys': {'a'}}, \
            module='gexecute', package_path=getcwd())
    {'a': 1}

    >>> gexec(func='__subset_dictionary', \
            params={'dict_': {'a': 1, 'b': 2}, 'subset_keys': {'a'}, 'junk': 'shouldn\\'t show up'}, \
            module='gexecute', package_path=getcwd())
    {'a': 1}
    """

    if not isinstance(params, dict):
        raise TypeError('{0} not supported for <params>! Needs to be a dictionary!'.format(type(params)))
    elif not isinstance(module, str) and not ismodule(module) and module is not None:
        raise TypeError('{0} not supported for <module>! Needs be either a module object or string!'.format(type(module)))
    elif not isinstance(package_path, str) and package_path is not None:
        raise TypeError('{0} not supported for <package path>! Needs to be a string!'.format(package_path))

    if not isfunction(func):
        # <func> is not a Function Object
        func = __get_function_obj(func=func, module=module, package_path=package_path)

    valid_params = __get_valid_input(func=func, params=params)

    call_function = '{function}({parameters})'.format(function=func.__name__, parameters=', '.join(['{key}={value}'.format(key=key, value=valid_parameters[key]) for key in valid_parameters]))
    logging.info(call_function)

    return func(**valid_params)
