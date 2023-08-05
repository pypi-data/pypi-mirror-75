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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.DownsampleImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.DownsampleImport$Builder")


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
def builder(db, namespace, table, timestampColumn, period, *keyColumns):
    return DownsampleImportBuilder(db, namespace, table, timestampColumn, period, *keyColumns)


class DownsampleImportBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (db, namespace, table, timestampColumn, period, *keyColumns)
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

    def addAggregate(self, aggType, column):
        return DownsampleImportBuilder(builder=self._builder.addAggregate(aggType, column))

    def addAggregates(self, *aggregates):
        return DownsampleImportBuilder(builder=self._builder.addAggregates(*aggregates))

    def addArrayColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addArrayColumns(*columns))

    def addAvgColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addAvgColumns(*columns))

    def addFirstColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addFirstColumns(*columns))

    def addLastColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addLastColumns(*columns))

    def addMaxColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addMaxColumns(*columns))

    def addMinColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addMinColumns(*columns))

    def addStdColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addStdColumns(*columns))

    def addSumColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addSumColumns(*columns))

    def addVarColumns(self, *columns):
        return DownsampleImportBuilder(builder=self._builder.addVarColumns(*columns))

    def build(self):
        return self._builder.build()

    def setAJStrategy(self, ajStrategy):
        return DownsampleImportBuilder(builder=self._builder.setAJStrategy(ajStrategy))

    def setAllBins(self, allBins):
        return DownsampleImportBuilder(builder=self._builder.setAllBins(allBins))

    def setByStrategy(self, byStrategy):
        return DownsampleImportBuilder(builder=self._builder.setByStrategy(byStrategy))

    def setCalendar(self, calendar):
        return DownsampleImportBuilder(builder=self._builder.setCalendar(calendar))

    def setDestinationDirectory(self, destinationDirectory):
        return DownsampleImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

    def setDestinationPartitions(self, destinationPartitions):
        return DownsampleImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setLogger(self, logger):
        return DownsampleImportBuilder(builder=self._builder.setLogger(logger))

    def setMaintainStateColumns(self, *maintainStateColumns):
        return DownsampleImportBuilder(builder=self._builder.setMaintainStateColumns(*maintainStateColumns))

    def setNaturalJoinStrategy(self, naturalJoinStrategy):
        return DownsampleImportBuilder(builder=self._builder.setNaturalJoinStrategy(naturalJoinStrategy))

    def setNumThreads(self, numThreads):
        return DownsampleImportBuilder(builder=self._builder.setNumThreads(numThreads))

    def setOutputMode(self, outputMode):
        return DownsampleImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        return DownsampleImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setSchemaService(self, schemaService):
        return DownsampleImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSourceName(self, sourceName):
        return DownsampleImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setSourceTable(self, sourceTable):
        return DownsampleImportBuilder(builder=self._builder.setSourceTable(sourceTable))

    def setStrict(self, strict):
        return DownsampleImportBuilder(builder=self._builder.setStrict(strict))

    def setTimeBinMode(self, timeBinMode):
        return DownsampleImportBuilder(builder=self._builder.setTimeBinMode(timeBinMode))
