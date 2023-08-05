#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

"""
Main Deephaven python module.

For convenient usage in the python console, the main sub-packages of deephaven have been imported here with aliases:
* Calendars imported as cals
* ComboAggregateFactory imported as caf
* DBTimeUtils imported as dbtu
* MovingAverages imported as mavg
* npy as npy
* Plot imported as plt
* QueryScope imported as qs
* TableManagementTools imported as tmt
* TableTools imported as ttools *(`tt` is frequently used for time table)*

Additionally, the following methods have been imported into the main deephaven namespace:
* from Plot import figure_wrapper as figw
* from java_to_python import tableToDataFrame, columnToNumpyArray, convertJavaArray
* from python_to_java import dataFrameToTable, createTableFromData
* from conversion_utils import convertToJavaArray, convertToJavaList, convertToJavaArrayList,
       convertToJavaHashSet, convertToJavaHashMap
* from ExportTools import JdbcLogger, TableLoggerBase
* from ImportTools import CsvImport, DownsampleImport, JdbcHelpers, JdbcImport, JsonImport,
       MergeData, XmlImport
* from InputTableTools import InputTable, TableInputHandler, LiveInputTableEditor
* from TableManipulation import ColumnRenderersBuilder, DistinctFormatter,
       DownsampledWhereFilter, LayoutHintBuilder, PersistentQueryTableHelper, PivotWidgetBuilder,
       SmartKey, SortPair, TotalsTableBuilder, WindowCheck

For ease of namespace population in a python console, consider::
>>> from deephaven import *  # this will import the submodules into the main namespace
>>> print(dir())  # this will display the contents of the main namespace
>>> help(plt)  # will display the help entry (doc strings) for the illumon.iris.plot module
>>> help(columnToNumpyArray)  # will display the help entry for the columnToNumpyArray method
"""

__all__ = [
    "PythonFunction", "PythonListenerAdapter", "PythonShiftAwareListenerAdapter",  # from here

    "DeephavenDb",  # from DeephavenDb

    "convertJavaArray", "tableToDataFrame", "columnToNumpyArray",  # from java_to_python

    "createTableFromData", "dataFrameToTable",  # from python_to_java

    "convertToJavaArray", "convertToJavaList", "convertToJavaArrayList", "convertToJavaHashSet",
    "convertToJavaHashMap",  # from conversion_utils

    'JdbcLogger',  'TableLoggerBase',  # from ExportTools

    'CsvImport', 'DownsampleImport', 'JdbcHelpers', 'JdbcImport', 'JsonImport', 'MergeData',
    'XmlImport',  # from ImportTools

    'InputTable', 'TableInputHandler', 'LiveInputTableEditor',  # from InputTableTools

    'ColumnRenderersBuilder', 'DistinctFormatter', 'DownsampledWhereFilter', 'LayoutHintBuilder',
    'PersistentQueryTableHelper', 'PersistentQueryControllerClient', 'PivotWidgetBuilder', 'SmartKey',
    'SortPair', 'TotalsTableBuilder', 'WindowCheck',  # from TableManipulation

    "cals", "caf", "dbtu", "figw", "mavg", "npy", "plt", "qs", "tmt", "ttools"  # subpackages with abbreviated names
]


import jpy
import sys
import base64  # builtin
import inspect

import wrapt  # dependencies
import dill

from .ImportTools import *
from .ExportTools import *
from .InputTableTools import *
from .TableManipulation import *

from .DeephavenDb import DeephavenDb
from .java_to_python import convertJavaArray, tableToDataFrame, columnToNumpyArray
from .python_to_java import dataFrameToTable, createTableFromData
from .conversion_utils import convertToJavaArray, convertToJavaList, convertToJavaArrayList, convertToJavaHashSet, \
    convertToJavaHashMap, getJavaClassObject

from . import Calendars as cals, \
    ComboAggregateFactory as caf, \
    DBTimeUtils as dbtu, \
    MovingAverages as mavg, \
    npy, \
    Plot as plt, \
    QueryScope as qs, \
    TableManagementTools as tmt, \
    TableTools as ttools

from .Plot import figure_wrapper as figw


# NB: this must be defined BEFORE importing .jvm_init or .start_jvm (circular import)
def initialize():
    __initializer__(jpy.get_type("com.fishlib.configuration.Configuration"), Config)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remotequery.RemoteQueryClient"), RemoteQueryClient)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery"), PythonRemoteQuery)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult"), PythonRemoteQueryPickledResult)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonPushClassQuery"), PythonPushClassQuery)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonEvalQuery"), PythonEvalQuery)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remote.RemoteDatabase"), RemoteDatabase)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable"), Inflatable)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage"), ExportedTableDescriptorMessage)
    __initializer__(jpy.get_type("com.illumon.integrations.python.PythonListenerAdapter"), PythonListenerAdapter)
    __initializer__(jpy.get_type("com.illumon.integrations.python.PythonFunction"), PythonFunction)

    # ensure that all the symbols are called and reimport the broken symbols
    cals.defineSymbols()
    caf.defineSymbols()
    dbtu.defineSymbols()
    mavg.defineSymbols()
    plt.defineSymbols()
    figw.defineSymbols()
    qs.defineSymbols()
    tmt.defineSymbols()
    ttools.defineSymbols()
    import deephaven.npy.table2numpy
    deephaven.npy.table2numpy.defineSymbols()

    import deephaven.ExportTools
    deephaven.ExportTools.defineSymbols()
    global TableLoggerBase
    from deephaven.ExportTools import TableLoggerBase
    JdbcLogger.defineSymbols()

    CsvImport.defineSymbols()
    DownsampleImport.defineSymbols()
    JdbcHelpers.defineSymbols()
    JdbcImport.defineSymbols()
    JsonImport.defineSymbols()
    MergeData.defineSymbols()
    XmlImport.defineSymbols()

    import deephaven.InputTableTools
    deephaven.InputTableTools.defineSymbols()
    global LiveInputTableEditor
    from deephaven.InputTableTools import LiveInputTableEditor
    InputTable.defineSymbols()
    TableInputHandler.defineSymbols()

    import deephaven.TableManipulation
    deephaven.TableManipulation.defineSymbols()
    global ColumnRenderersBuilder, DistinctFormatter, DownsampledWhereFilter, LayoutHintBuilder, \
        PivotWidgetBuilder, SmartKey, SortPair, TotalsTableBuilder
    from deephaven.TableManipulation import ColumnRenderersBuilder, DistinctFormatter, \
        DownsampledWhereFilter, LayoutHintBuilder, PivotWidgetBuilder, SmartKey, SortPair, \
        TotalsTableBuilder

    PersistentQueryTableHelper.defineSymbols()
    WindowCheck.defineSymbols()

    global Figure, PlottingConvenience
    Figure = FigureUnsupported
    PlottingConvenience = FigureUnsupported

    jpy.type_translations['com.illumon.iris.db.tables.remote.RemoteDatabase'] = wrap_db


from .jvm_init import jvm_init
from .start_jvm import start_jvm


Figure = None  # variable for initialization
PlottingConvenience = None  # variable for initialization


def verifyPicklingCompatibility(otherPythonVersion):
    """
    Check a provided python version string versus the present instance string for pickling safety.

    :param otherPythonVersion: other version string
    :return: True is safe, False otherwise
    """

    if otherPythonVersion is None:
        return False
    sPyVer = otherPythonVersion.split('.')
    if len(sPyVer) < 3:
        return False
    try:
        major, minor = int(sPyVer[0]), int(sPyVer[1])
        # We need both major and minor agreement for pickling compatibility
        return major == sys.version_info[0] and minor == sys.version_info[1]
    except Exception:
        return False


class DbWrapper(wrapt.ObjectProxy):
    def executeQuery(self, query):
        pickled = dill.dumps(query)
        newQuery = PythonRemoteQuery(pickled)  # note that the protocol flag doesn't help with cross compatibility
        res = self.__wrapped__.executeQuery(newQuery)
        return self.inflateResult(res)

    def pushClass(self, classToDefine):
        if not inspect.isclass(classToDefine):
            raise TypeError("{} is not a class!".format(classToDefine))

        name = classToDefine.__name__
        pickled = dill.dumps(classToDefine)
        pushQuery = PythonPushClassQuery(name, pickled)
        self.__wrapped__.executeQuery(pushQuery)

    def eval(self, string):
        evalQuery = PythonEvalQuery(string)
        self.__wrapped__.executeQuery(evalQuery)

    def fetch(self, name):
        fetchQuery = PythonEvalQuery(name)
        res = self.__wrapped__.executeQuery(fetchQuery)
        return self.inflateResult(res)

    def inflateResult(self, obj):
        if isinstance(obj, jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable")):
            return obj.inflate(self.__wrapped__.getProcessorConnection())
        elif isinstance(obj, jpy.get_type("com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage")):
            return obj.inflate(self.__wrapped__.getProcessorConnection())
        elif isinstance(obj, jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult")):
            if not verifyPicklingCompatibility(obj.getPythonVersion()):
                raise RuntimeError("Attempting to inflate a result pickled using a python version instance {} "
                                   "on the present python version instance {}. These versions are incompatible for "
                                   "serialization/pickling.".format(obj.getPythonVersion(), sys.version))
            return dill.loads(base64.b64decode(obj.getPickled()))
        else:
            return obj

    def importClass(self, classToImport):
        if isinstance(classToImport, str):
            classToImport = getJavaClassObject(classToImport)
        elif hasattr(classToImport, 'jclass'):
            classToImport = classToImport.jclass
        self.__wrapped__.importClass(classToImport)


class FigureUnsupported(object):
    def __init__(self):
        raise Exception("Can not create a plot outside of the console.")


def __initializer__(jtype, obj):
    for key, value in jtype.__dict__.items():
        obj.__dict__.update({key: value})


def wrap_db(type, obj):
    return DbWrapper(obj)


def AuthenticationManager():
    return jpy.get_type("com.fishlib.auth.WAuthenticationClientManager")


def RemoteQueryClient(*args):
    jtype = jpy.get_type("com.illumon.iris.db.tables.remotequery.RemoteQueryClient")
    if len(args) > 2:
        return jtype(args[:3])
    else:
        return jtype(*args)


def PythonRemoteQuery(dilledObject):
    return jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery")(dilledObject, sys.version)


def PythonRemoteQueryPickledResult(pickled):
    return jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult")(pickled, sys.version)


def PythonPushClassQuery(name, dilledObject):
    return jpy.get_type("com.illumon.iris.db.util.PythonPushClassQuery")(name, dilledObject, sys.version)


def PythonEvalQuery(string):
    return jpy.get_type("com.illumon.iris.db.util.PythonEvalQuery")(string)


def RemoteDatabase(processorConnection):
    return jpy.get_type("com.illumon.iris.db.tables.remote.RemoteDatabase")(processorConnection)


def Inflatable():  # what purpose does this serve?
    return jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable")


def ExportedTableDescriptorMessage(id):
    return jpy.get_type("com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage")(id)


def Config():
    return jpy.get_type("com.fishlib.configuration.Configuration").getInstance()


def PythonListenerAdapter(dynamicTable, implementation, description=None, retain=True, replayInitialImage=False):
    """
    Constructs the InstrumentedListenerAdapter, implemented in Python, and plugs it into the table's
    listenForUpdates method.

    :param dynamicTable: table to which to listen - NOTE: it will be cast to DynamicTable.
    :param implementation: the body of the implementation for the InstrumentedListenerAdapter.onUpdate method, and
      must either be a class with onUpdate method or a callable.
    :param description: A description for the UpdatePerformanceTracker to append to its entry description.
    :param retain: Whether a hard reference to this listener should be maintained to prevent it from being collected.
    :param replayInitialImage: False to only process new rows, ignoring any previously existing rows in the Table;
      True to process updates for all initial rows in the table PLUS all new row changes.
    """

    jtype = jpy.get_type('com.illumon.integrations.python.PythonListenerAdapter')
    # Construct our Listener
    ListenerInstance = jtype(description, dynamicTable, retain, implementation)
    # Plug it in to the dynamic table
    if hasattr(dynamicTable, 'listenForUpdates'):
        dynamicTable.listenForUpdates(ListenerInstance, replayInitialImage)
    else:
        # We have to cast it as a dynamic table
        jpy.cast(dynamicTable, jpy.get_type('com.illumon.iris.db.v2.DynamicTable'))\
            .listenForUpdates(ListenerInstance, replayInitialImage)


def PythonShiftAwareListenerAdapter(dynamicTable, implementation, description=None, retain=True):
    """
    Constructs the InstrumentedShiftAwareListenerAdapter, implemented in Python, and plugs it into the table's
    listenForUpdates method.

    :param dynamicTable: table to which to listen - NOTE: it will be cast to DynamicTable.
    :param implementation: the body of the implementation for the InstrumentedShiftAwareListenerAdapter.onUpdate method, and
      must either be a class with onUpdate method or a callable.
    :param description: A description for the UpdatePerformanceTracker to append to its entry description.
    :param retain: Whether a hard reference to this listener should be maintained to prevent it from being collected.
    """

    jtype = jpy.get_type('com.illumon.integrations.python.PythonShiftAwareListenerAdapter')
    # Construct our Listener
    ListenerInstance = jtype(description, dynamicTable, retain, implementation)
    # Plug it in to the dynamic table
    if hasattr(dynamicTable, 'listenForUpdates'):
        dynamicTable.listenForUpdates(ListenerInstance)
    else:
        # We have to cast it as a dynamic table
        jpy.cast(dynamicTable, jpy.get_type('com.illumon.iris.db.v2.DynamicTable'))\
            .listenForUpdates(ListenerInstance)


def PythonFunction(func, classString):
    """
    Constructs a Java Function<PyObject, Object> implementation from the given python function `func`. The proper
    Java object interpretation for the return of `func` must be provided.

    :param func: Python callable or class instance with `apply` method (single argument)
    :param classString: the fully qualified class path of the return for `func`. This is really anticipated to be one
                        of `java.lang.String`, `double`, 'float`, `long`, `int`, `short`, `byte`, or `boolean`,
                        and any other value will result in `java.lang.Object` and likely be unusable.
    :return: com.illumon.integrations.python.PythonFunction instance, primarily intended for use in PivotWidgetBuilder usage
    """

    jtype = jpy.get_type('com.illumon.integrations.python.PythonFunction')
    return jtype(func, getJavaClassObject(classString))
