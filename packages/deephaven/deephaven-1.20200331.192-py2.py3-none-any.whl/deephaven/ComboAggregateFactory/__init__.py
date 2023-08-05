#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first defineSymbols() call


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.db.v2.by.ComboAggregateFactory")


# every module method should be decorated with @_passThrough
@wrapt.decorator
def _passThrough(wrapped, instance, args, kwargs):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    defineSymbols()
    return wrapped(*args, **kwargs)


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@_passThrough
def Agg(*args):
    return _java_type_.Agg(*args)


@_passThrough
def AggAbsSum(*matchPairs):
    return _java_type_.AggAbsSum(*matchPairs)


@_passThrough
def AggArray(*matchPairs):
    return _java_type_.AggArray(*matchPairs)


@_passThrough
def AggAvg(*matchPairs):
    return _java_type_.AggAvg(*matchPairs)


@_passThrough
def AggCombo(*aggregations):
    return _java_type_.AggCombo(*aggregations)


@_passThrough
def AggCount(resultColumn):
    return _java_type_.AggCount(resultColumn)


@_passThrough
def AggFirst(*matchPairs):
    return _java_type_.AggFirst(*matchPairs)


@_passThrough
def AggFormula(formula, formulaParam, *matchPairs):
    return _java_type_.AggFormula(formula, formulaParam, *matchPairs)


@_passThrough
def AggLast(*matchPairs):
    return _java_type_.AggLast(*matchPairs)


@_passThrough
def AggMax(*matchPairs):
    return _java_type_.AggMax(*matchPairs)


@_passThrough
def AggMed(*matchPairs):
    return _java_type_.AggMed(*matchPairs)


@_passThrough
def AggMin(*matchPairs):
    return _java_type_.AggMin(*matchPairs)


@_passThrough
def AggPct(*args):
    return _java_type_.AggPct(*args)


@_passThrough
def AggStd(*matchPairs):
    return _java_type_.AggStd(*matchPairs)


@_passThrough
def AggSum(*matchPairs):
    return _java_type_.AggSum(*matchPairs)


@_passThrough
def AggVar(*matchPairs):
    return _java_type_.AggVar(*matchPairs)


@_passThrough
def AggWAvg(weight, *matchPairs):
    return _java_type_.AggWAvg(weight, *matchPairs)
