#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonImportTools" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first defineSymbols() call
_builder_type_ = None  # None until the first defineSymbols() call


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _builder_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.JdbcImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.JdbcImport$Builder")


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
def builder(namespace, table):
    return JdbcImportBuilder(namespace, table)


@_passThrough
def getServerTimeZone(driver, connectionUrl, user, password):
    return _java_type_.getServerTimeZone(driver, connectionUrl, user, password)


class JdbcImportBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (namespace, table)
        - **kwargs, when provided, should take the form {'builder': *value*}, and is generally 
          meant for internal use
        """
        defineSymbols()
        builder = kwargs.get('builder', None)
        if builder is not None:
            self._builder = builder
        else:
            self._builder = _java_type_.builder(*args)

    @property
    def builder(self):
        """The actual java builder object"""
        return self._builder

    def build(self):
        return self._builder.build()

    def setConnectionUrl(self, connectionUrl):
        return JdbcImportBuilder(builder=self._builder.setConnectionUrl(connectionUrl))

    def setDestinationDirectory(self, destinationDirectory):
        return JdbcImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

    def setDestinationPartitions(self, destinationPartitions):
        return JdbcImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setDriver(self, driver):
        return JdbcImportBuilder(builder=self._builder.setDriver(driver))

    def setOutputMode(self, outputMode):
        return JdbcImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        return JdbcImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setPassword(self, password):
        return JdbcImportBuilder(builder=self._builder.setPassword(password))

    def setQuery(self, query):
        return JdbcImportBuilder(builder=self._builder.setQuery(query))

    def setSchemaService(self, schemaService):
        return JdbcImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSourceName(self, sourceName):
        return JdbcImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setSourceTimeZone(self, *args):
        return JdbcImportBuilder(builder=self._builder.setSourceTimeZone(*args))

    def setStrict(self, strict):
        return JdbcImportBuilder(builder=self._builder.setStrict(strict))

    def setUser(self, user):
        return JdbcImportBuilder(builder=self._builder.setUser(user))
