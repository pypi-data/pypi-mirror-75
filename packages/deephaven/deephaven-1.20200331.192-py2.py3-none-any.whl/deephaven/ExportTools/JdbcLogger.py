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
        _java_type_ = jpy.get_type("com.illumon.iris.export.jdbc.JdbcLogger")
        _builder_type_ = jpy.get_type("com.illumon.iris.export.jdbc.JdbcLogger$Builder")


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
def builder(*args):
    """
    *Overload 1*  
      :param logger: com.fishlib.io.logger.Logger
      :param jdbcDriver: java.lang.String
      :param jdbcUrl: java.lang.String
      :param catalog: java.lang.String
      :param schema: java.lang.String
      :param tableName: java.lang.String
      :return: com.illumon.iris.export.jdbc.JdbcLogger.Builder
      
    *Overload 2*  
      :param logger: com.fishlib.io.logger.Logger
      :param jdbcDriver: java.lang.String
      :param jdbcUrl: java.lang.String
      :param schema: java.lang.String
      :param tableName: java.lang.String
      :return: com.illumon.iris.export.jdbc.JdbcLogger.Builder
      
    *Overload 3*  
      :param logger: com.fishlib.io.logger.Logger
      :param jdbcDriver: java.lang.String
      :param jdbcUrl: java.lang.String
      :param tableName: java.lang.String
      :return: com.illumon.iris.export.jdbc.JdbcLogger.Builder
    """
    
    return JdbcLoggerBuilder(*args)


class JdbcLoggerBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (*args)
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

    def batchSize(self, batchSize):
        """
        Specify the batch size when writing to the JDBC data source. For efficiency, the JDBC logger "batches" SQL
         statements when possible. Each Deephaven table update results in at least one commit, regardless of the
         batch size, so this represents a maximum. The default batch size is 500 rows.
        
         Batching is only effective when the TableLoggerBase.Flags setting is not "RowByRow", since that
         effectively requires a commit for every row. When logging with updates, the "Atomic" setting is recommended,
         which requires only one commit for each Deephaven table update (which can affect any number of rows). When
         logging snapshots only, any setting other than "RowByRow" will take advantage of batching.
        
        :param batchSize: (int) - the maximum batch size (legal range is 1 to 100,000)
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.batchSize(batchSize))

    def build(self):
        """
        Creates a JdbcLogger with configuration specified by arguments to the builder.
        
        :return: (com.illumon.iris.export.jdbc.JdbcLogger) a new JdbcLogger
        """
        
        return self._builder.build()

    def calendar(self, calendar):
        """
        Specify the Calendar to use when logging to JDBC date/datetime/timestamp columns. This can affect the way
         DateTime values are logged when the target column does not directly store an offset/timezone.
         See PreparedStatement.setDate(int, Date, Calendar) and
         PreparedStatement.setTimestamp(int, Timestamp, Calendar) (int, Date, Calendar)} for details.
        
        :param calendar: (java.util.Calendar) - the Calendar to use for logging
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.calendar(calendar))

    def dataColumn(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Add a data column for logging, with the same name in the source and target.
        
        *Overload 1*  
          :param targetColumn: (java.lang.String) - the column name
          :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
          
        *Overload 2*  
          :param targetColumn: (java.lang.String) - column name in the JDBC table
          :param sourceColumn: (java.lang.String) - column name in the source Deephaven table
          :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.dataColumn(*args))

    def jdbcPassword(self, jdbcPassword):
        """
        Specify the JDBC database password. Only necessary if not specified as part of the JDBC URL.
        
        :param jdbcPassword: (java.lang.String) - JDBC database password
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.jdbcPassword(jdbcPassword))

    def jdbcUser(self, jdbcUser):
        """
        Specify the JDBC database user. Only necessary if not specified as part of the JDBC URL.
        
        :param jdbcUser: (java.lang.String) - JDBC database user name
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.jdbcUser(jdbcUser))

    def keyColumns(self, *keyColumns):
        """
        Specify the set of columns that represent the primary key when logging to JDBC. This set of column(s) will be
         used in order to generate the WHERE clause in UPDATE and DELETE operations, when not in "log mode". If in log
         mode, key columns are unnecessary, since every source table update will simply be logged as an INSERT to the
         JDBC target.
        
         The key columns should be either composed of a subset of the data columns (as they are named in the SQL
         table), or the rowIndex column. Each set of unique values in these columns should represent a unique row in
         order for logging to work properly. If present, a rowIndex column always provides this feature.
        
        :param keyColumns: (java.lang.String...) - an array of columns to use as the composite primary key
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.keyColumns(*keyColumns))

    def logMode(self, logMode):
        """
        Set log mode indicator. If not specified, this defaults to false.
        
         When in log mode, each update to the source Deephaven table will result in an INSERT into the target table
         (i.e. the target will be an append-only log of every update to the source).
        
         Otherwise, each operation is replicated in the target using the appropriate INSERT/UPDATE/DELETE operation,
         using the specified row key columns to uniquely identify rows.
        
        :param logMode: (boolean) - if true, run in log mode
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.logMode(logMode))

    def operationColumn(self, operationColumn):
        """
        Specify the JDBC column that will receive the operation that resulted in that row. This is most useful in
         "log mode", in order to differentiate between Added/ModifiedOld/ModifiedNew/Removed operations in the source
         table. A PreparedStatement.setString(int, java.lang.String) will be used to set this value, so the target column
         should be a VARCHAR with length 11 or more.
        
        :param operationColumn: (java.lang.String) - the JDBC column that will receive the operation (must be compatible with a string value)
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.operationColumn(operationColumn))

    def rowIndexColumn(self, rowIndexColumn):
        """
        Specify the JDBC column that will receive the rowIndex of the source table row that resulted in a given
         JDBC row. A PreparedStatement.setLong(int, long) will be used to set this value, so the target column
         should be an SQL BIGINT or equivalent.
        
        :param rowIndexColumn: (java.lang.String) - the JDBC column that will receive the operation (must be compatible with 64 bit integer)
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) the Builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.rowIndexColumn(rowIndexColumn))
