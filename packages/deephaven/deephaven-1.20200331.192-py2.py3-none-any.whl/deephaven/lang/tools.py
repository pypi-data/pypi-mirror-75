# When analyzing / generating ast produced by ast.parse(),
# you can use these helper functions to do whatever you need.
# Any common / reusable functionality should go here.

from _ast import Load, Store, Name, Param, Call, keyword, Subscript, FunctionDef, arguments, Index, Num, Attribute, \
    Assign, AST, If, Compare, Is, Str, List
from numpy import int32, int64, float32, float64, asarray, empty, dtype
from numba.types import Type, int_, float_, complex128
from re import compile
from sys import version_info
is_py2 = version_info[0] < 3
_regex_int_or_float = compile(r"^(int|float)([0-9]+)$")


class not_py3:
    """We need to import some ast types that only exist in py3,
    and we want to isinstance() check some variables against those types.
    So, we'll use this junk class in python 2 and real imports for python 3."""
    pass


arg = not_py3
NameConstant = not_py3

if not is_py2:
    from _ast import arg, NameConstant


def array_access(var_name, index):
    var_name = read(var_name)
    # var_name if isinstance(var_name, AST) else read(var_name) if is_py2 else arg(arg=var_name, annotation=None)
    index = index if isinstance(index, AST) else Num(index)
    return Subscript(value=var_name, ctx=Load(), slice=Index(value=index))


def write_array(var_name, index):
    var_name = read(var_name)
    index = index if isinstance(index, AST) else Num(index)
    return Subscript(value=var_name, ctx=Store(), slice=Index(value=index))


def read(name):
    return Name(id=name.id, ctx=Load()) if isinstance(name, Name) else \
        name_constant(name) if isinstance(name, str) else \
        Name(id=name.arg, ctx=Load()) if isinstance(name, arg) else name


def name_constant(name):
    """Python 3 uses NameConstant for True, False and None,
    while python 2 uses (assignable) variables named "True", "False" and "None"."""
    return Name(id=name, ctx=Load()) if is_py2 else \
        NameConstant(value=True) if 'True' == name else \
        NameConstant(value=False) if 'False' == name else \
        NameConstant(value=None) if 'None' == name else \
        Name(id=name, ctx=Load())


def read_none():
    return Name(id='None', ctx=Load()) if is_py2 else NameConstant(value=None)


def read_true():
    return Name(id='True', ctx=Load()) if is_py2 else NameConstant(value=True)


def read_false():
    return Name(id='False', ctx=Load()) if is_py2 else NameConstant(value=False)


def write(name):
    return Name(id=name, ctx=Store())


def keyword_arg(name, value):
    value = value if isinstance(value, AST) else Str(value)
    return keyword(arg=name, value=value)


def field_read(scope, field):
    scope = scope if isinstance(scope, AST) or isinstance(scope, arg) else read(scope)
    return Attribute(value=scope, attr=field, ctx=Load())


def decorate(fun, args):
    """Create a decorator call.  To get jit(nopython=True), call decorate('jit', {"nopython": "True"}"""
    return Call(func=Name(id=fun, ctx=Load()), args=[],
                keywords=list(map(lambda kv:
                                  keyword(arg=kv[0],
                                          value=read(kv[1])),
                                  itr(args))),
                starargs=None, kwargs=None)


def method_call(scope, args, keywords=None):
    scope = scope if isinstance(scope, AST) else read(scope)
    args = list(map(lambda x: x if isinstance(x, AST) or isinstance(x, arg) else read(x), args))
    return Call(func=scope,
                args=args,
                keywords=[] if keywords is None else keywords,
                starargs=None, kwargs=None)


def assign(target, value):
    # Convert strings to Name(id=target, ctx=Store())
    target = target if isinstance(target, AST) else write(target)
    return Assign(targets=[target], ctx=Load(), value=value)


def param(name):
    return name if isinstance(name, Name) else Name(id=name.arg, ctx=Param())


def arg_or_name(name, name_ctx=Param()):
    return Name(id=name, ctx=name_ctx) if is_py2 else arg(arg=name, annotation=None)


def to_ast(item):
    if isinstance(item, list):
        return list(map(lambda i: to_ast(i), item))
    return item if isinstance(item, AST) \
        else Str(s=item) if isinstance(item, str) \
        else Num(n=item)


def new_list(items):
    return List(ctx=Load(),
                elts=to_ast(items) if isinstance(items, list) else [to_ast(items)])


def new_func(func_name, args, body, decorators=None, defaults=None):
    return FunctionDef(name=func_name,
                       returns=None,
                       args=arguments(args=args, vararg=None, kwarg=None,
                                      kw_defaults=[],
                                      kwonlyargs=[],
                                      defaults=[] if defaults is None else defaults),
                       body=body,
                       decorator_list=[] if decorators is None else decorators)


def check_if_none(val, body, orelse=[]):
    val = val if isinstance(val, AST) else read(val)
    cmp = Compare(left=val, ops=[Is()], comparators=[read_none()])
    return If(test=cmp, body=body, orelse=orelse)


def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def int32_(a):
    return asarray(a, dtype=int32, order='C') if isinstance(a, list) \
        else empty(a, dtype=int32, order='C')


def int64_(a):
    return asarray(a, dtype=int64, order='C') if isinstance(a, list) \
        else empty(a, dtype=int64, order='C')


def float32_(a):
    return asarray(a, dtype=float32, order='C') if isinstance(a, list) \
        else empty(a, dtype=float32, order='C')


def float64_(a):
    return asarray(a, dtype=float64, order='C') if isinstance(a, list) \
        else empty(a, dtype=float64, order='C')


def to_numba_type(item_type):
    if isinstance(item_type, int):
        item_type = int_
    elif isinstance(item_type, float):
        item_type = float_
    elif isinstance(item_type, complex):
        item_type = complex128
    return item_type if isinstance(item_type, Type) else \
        int_ if isinstance(item_type, int) else \
        float_ if isinstance(item_type, float) else \
        complex128 if isinstance(item_type, complex) else \
        dtype(item_type)


def num_size(s):
    try:
        return int(_regex_int_or_float.sub(r'\2', s))
    except ValueError:
        return None


def int_or_float(s):
    return _regex_int_or_float.sub(r'\1', s)


def itr(arr):
    return arr.iteritems() if is_py2 else arr.items()


def values(dct):
    return list(dct.itervalues()) if is_py2 else list(dct.values())
