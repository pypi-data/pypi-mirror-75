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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.CsvImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.CsvImport$Builder")


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
    return CsvImportBuilder(namespace, table)


class CsvImportBuilder(object):
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

    def setColumnNames(self, columnNames):
        return CsvImportBuilder(builder=self._builder.setColumnNames(columnNames))

    def setConstantColumnValue(self, constantColumnValue):
        return CsvImportBuilder(builder=self._builder.setConstantColumnValue(constantColumnValue))

    def setDelimiter(self, delimiter):
        return CsvImportBuilder(builder=self._builder.setDelimiter(delimiter))

    def setDestinationDirectory(self, destinationDirectory):
        return CsvImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

    def setDestinationPartitions(self, destinationPartitions):
        return CsvImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setFileFormat(self, fileFormat):
        return CsvImportBuilder(builder=self._builder.setFileFormat(fileFormat))

    def setNoHeader(self, noHeader):
        return CsvImportBuilder(builder=self._builder.setNoHeader(noHeader))

    def setOutputMode(self, outputMode):
        return CsvImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        return CsvImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setSchemaService(self, schemaService):
        return CsvImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSkipFooterLines(self, skipFooterLines):
        return CsvImportBuilder(builder=self._builder.setSkipFooterLines(skipFooterLines))

    def setSkipLines(self, skipLines):
        return CsvImportBuilder(builder=self._builder.setSkipLines(skipLines))

    def setSourceDirectory(self, sourceDirectory):
        return CsvImportBuilder(builder=self._builder.setSourceDirectory(sourceDirectory))

    def setSourceFile(self, sourceFile):
        return CsvImportBuilder(builder=self._builder.setSourceFile(sourceFile))

    def setSourceGlob(self, sourceGlob):
        return CsvImportBuilder(builder=self._builder.setSourceGlob(sourceGlob))

    def setSourceName(self, sourceName):
        return CsvImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setStrict(self, strict):
        return CsvImportBuilder(builder=self._builder.setStrict(strict))

    def setTrim(self, trim):
        return CsvImportBuilder(builder=self._builder.setTrim(trim))
