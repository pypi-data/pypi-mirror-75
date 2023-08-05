import argparse
import inspect
import os
import re
import sys

"""
easy_argparser.py
====================================
The core module of my project
"""


arg_parse_args = {
    'VERSION': '1.0.0',
    'DESCRIPTION': '',
    'PROG': os.path.basename(__file__),
}


def command_line(self):
    """
    Autogenerate command line.
    """
    methods = inspect.getmembers(self, predicate=inspect.ismethod)
    v = '%(prog)s {version}'.format(version=self.arg_parse_args['VERSION'])
    my_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=v + " - " + self.arg_parse_args['DESCRIPTION'], prog=self.arg_parse_args['PROG']
    )
    functions = [i[0] for i in methods]
    all_params = {}
    for function in functions:
        if function == 'command_line': continue
        params = inspect.signature(eval('self.' + function)).parameters.values()
        param_names = [i.name for i in params if i.default == inspect._empty]
        optionals = [(i.name, i.default) for i in params if i.default != inspect._empty]
        all_params[function] = [param_names, optionals]
        if optionals or len(param_names) > 0:
            my_parser.add_argument("--" + function,
                                   nargs="*" if optionals else len(param_names) if len(param_names) > 0 else None,
                                   metavar=tuple(param_names) if param_names and not optionals
                                   else (' '.join(param_names), "") if param_names and optionals else None,
                                   help="Optional args: " + " ".join(["[{0}={1}]".format(*p)
                                                                      if p[1] else "[{0}]".format(p[0])
                                                                      for p in optionals])
                                   if len(optionals) > 0 else None)
        else:
            my_parser.add_argument('--' + function, action='store_true')

    args = my_parser.parse_args()
    for arg, value in args.__dict__.items():
        if len(all_params[arg][0]) == 0 and len(all_params[arg][1]) == 0 and not value:
            value = None
        if arg in functions and value is not None:
            self.called_function = function
            try:
                if len(all_params[arg][0]) == 0 and len(all_params[arg][1]) == 0:
                    res = eval('self.{0}()'.format(arg))
                else:
                    res = eval('self.' + arg)(*value)
            except Exception as e:
                raise e
            # exit(0)


def add_argparser():
    pass

# Ignore decorator to ignore a method class or variable

# decorator
def Cmdline(options):
    """
    Decorator to autogenerate command line.
    """
    def _cmdline(func):
        def wrapper(*inner_args, **kwargs):
            # print(enter_string)
            if options:
                arg_parse_args.update(options)
            setattr(func, 'arg_parse_args', arg_parse_args)
            setattr(func, 'command_line', command_line)
            return func(*inner_args, **kwargs)
            # print(exit_string)

        # if not inspect.isclass(func): raise Exception("Can only decorate classes")
        return wrapper

    return _cmdline


def cmdline(obj=None, options=None):
    """
    Call this to make your file a cmdline program

    :param obj:
    :param options:
    :return:
    """
    if not obj:
        modules = sys.modules.keys()
        obj = [i for i in globals() if i not in modules and not re.match('__.*__', i)]
        print(obj)


if __name__ == '__main__':
    # a = inspect.getmembers()
    # a = [func for func in dir()]
    # print(a)
    # print(sys.modules.keys())
    cmdline()

#
# @cmdline(OPTIONS={
#     'DESCRIPTION': 'description test'
# })
# class A:
#     a = 'something'
#
#     def imcool(self):
#         print('i"m cool')
#
#     def say(self, something):
#         print(something)
#
#
# A().command_line()
