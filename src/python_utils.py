''' Python functions designed to import Python objects into lisp environment'''
import importlib


def load_module(module, env=None):
    '''(load-py 'module_name)'''
    mod = importlib.import_module(module)
    env.update(vars(mod))


def from_module_load(module, *names, env=None):
    '''(from-py-load 'module_name 'var1 'var2 ...)'''
    mod = importlib.import_module(module)
    for name in names:
        env.update({name: getattr(mod, name)})


def from_module_load_variable_as(module, *names, env=None):
    '''(from-py-load-as 'module_name '(var1 name1) '(var2 name2) ...)'''
    mod = importlib.import_module(module)
    for name, name_as in names:
        env.update({name_as: getattr(mod, name)})


def with_instance(inst, attr, *args):
    '''(with-py-inst instance 'attribute OR method arg1 arg 2 ...)'''
    if hasattr(inst, attr):
        attr = getattr(inst, attr)
        if callable(attr):
            return attr(*args)
        else:
            return attr
    else:
        print("{} has no attribute {}.".format(inst, attr))


python_fns = {
    'load-py': load_module,
    'from-py-load': from_module_load,
    'from-py-load-as': from_module_load_variable_as,
    'with-py-inst': with_instance
}
