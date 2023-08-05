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
        _java_type_ = jpy.get_type("com.illumon.iris.db.tables.select.QueryScope")


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
def addParam(name, value):
    """
    Note: Java generics information - <T>
    
    :param name: java.lang.String
    :param value: T
    """
    
    return _java_type_.addParam(name, value)


@_passThrough
def getDefaultInstance():
    """
    :return: com.illumon.iris.db.tables.select.QueryScope
    """
    
    return _java_type_.getDefaultInstance()


@_passThrough
def getParamValue(name):
    """
    Note: Java generics information - <T>
    
    :param name: java.lang.String
    :return: T
    """
    
    return _java_type_.getParamValue(name)


@_passThrough
def makeScriptSessionImpl(scriptSession):
    return _java_type_.makeScriptSessionImpl(scriptSession)


@_passThrough
def setDefaultInstance(queryScope):
    """
    :param queryScope: com.illumon.iris.db.tables.select.QueryScope
    """
    
    return _java_type_.setDefaultInstance(queryScope)
