#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

"""
Module containing a few different classes for table display options and manipulation.
"""

import jpy
from ._PersistentQueryControllerClient import PersistentQueryControllerClient

__all__ = ['ColumnRenderersBuilder', 'DistinctFormatter', 'DownsampledWhereFilter', 'LayoutHintBuilder',
           'PersistentQueryTableHelper', 'PersistentQueryControllerClient', 'PivotWidgetBuilder',
           'SmartKey', 'SortPair', 'TotalsTableBuilder', 'WindowCheck']

# None until the first successful defineSymbols() call
ColumnRenderersBuilder = None
DistinctFormatter = None
DownsampledWhereFilter = None
LayoutHintBuilder = None
PivotWidgetBuilder = None
SmartKey = None
TotalsTableBuilder = None
SortPair = None


def defineSymbols():
    """
    Defines appropriate java symbols, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global ColumnRenderersBuilder, DistinctFormatter, DownsampledWhereFilter, LayoutHintBuilder, \
        PivotWidgetBuilder, SmartKey, TotalsTableBuilder, SortPair

    if ColumnRenderersBuilder is None:
        # This will raise an exception if the desired object is not the classpath
        ColumnRenderersBuilder = jpy.get_type('com.illumon.iris.db.v2.ColumnRenderersBuilder')
        DistinctFormatter = jpy.get_type('com.illumon.iris.db.util.DBColorUtil$DistinctFormatter')
        DownsampledWhereFilter = jpy.get_type('com.illumon.iris.db.v2.select.DownsampledWhereFilter')
        LayoutHintBuilder = jpy.get_type('com.illumon.iris.db.tables.utils.LayoutHintBuilder')
        PivotWidgetBuilder = jpy.get_type('com.illumon.iris.console.utils.PivotWidgetBuilder')
        SmartKey = jpy.get_type('com.fishlib.datastructures.util.SmartKey')
        TotalsTableBuilder = jpy.get_type('com.illumon.iris.db.v2.TotalsTableBuilder')
        SortPair = jpy.get_type("com.illumon.iris.db.tables.SortPair")


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass
