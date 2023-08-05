#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

######################################################################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonFigureWrapper or "./gradlew :Generators:generatePythonFigureWrapper" to generate
######################################################################################################################


import sys
import logging
import jpy
import numpy
import pandas
import wrapt

from ..conversion_utils import _isJavaType, _isStr, makeJavaArray, _ensureBoxedArray, getJavaClassObject


_plotting_convenience_ = None  # this module will be useless with no jvm
_figure_widget_ = None


def defineSymbols():
    """
    Defines appropriate java symbols, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _plotting_convenience_, _figure_widget_
    if _plotting_convenience_ is None:
        # an exception will be raised if not in the jvm classpath
        _plotting_convenience_ = jpy.get_type("com.illumon.iris.db.plot.PlottingConvenience")
        _figure_widget_ = jpy.get_type('com.illumon.iris.db.plot.FigureWidget')


if sys.version_info[0] > 2:
    def _is_basic_type_(obj):
        return isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str)
else:
    def _is_basic_type_(obj):
        return isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, long) \
               or isinstance(obj, float) or isinstance(obj, basestring)


def _is_widget_(obj):
    if obj is None:
        return False
    cond = False
    try:
        cond = getJavaClassObject('com.illumon.iris.db.plot.FigureWidget').isAssignableFrom(obj)
    except Exception:
        pass
    return cond


def _create_java_object_(obj):
    if obj is None:
        return None
    elif isinstance(obj, FigureWrapper) or _isJavaType(obj):
        # nothing to be done
        return obj
    elif _is_basic_type_(obj):
        # jpy will (*should*) convert this properly
        return obj
    elif isinstance(obj, numpy.ndarray) or isinstance(obj, pandas.Series) or isinstance(obj, pandas.Categorical):
        return makeJavaArray(obj, 'unknown', False)
    elif isinstance(obj, dict):
        return obj  # what would we do?
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return _create_java_object_(numpy.array(obj))  # maybe it's better to pass it straight through?
    elif hasattr(obj, '__iter__'):
        # return _create_java_object_(numpy.array(list(obj))) # this is suspect
        return obj
    else:
        # I have no idea what it is - just pass it straight through
        return obj


def _convert_arguments_(args):
    return [_create_java_object_(el) for el in args]


@wrapt.decorator
def _convertArguments(wrapped, instance, args, kwargs):
    """
    For decoration of FigureWrapper class methods, to convert arguments as necessary

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    return wrapped(*_convert_arguments_(args))


@wrapt.decorator
def _convertCatPlotArguments(wrapped, instance, args, kwargs):
    """
    For decoration of FigureWrapper catPlot, catErrorBar, piePlot method, to convert arguments

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    cargs = _convert_arguments_(args)
    cargs[1] = _ensureBoxedArray(cargs[1])  # the category field must extend Number (i.e. be boxed)
    return wrapped(*cargs)


@wrapt.decorator
def _convertCatPlot3dArguments(wrapped, instance, args, kwargs):
    """
    For decoration of FigureWrapper catPlot3d method, to convert arguments as necessary

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    cargs = _convert_arguments_(args)
    cargs[1] = _ensureBoxedArray(cargs[1])
    cargs[2] = _ensureBoxedArray(cargs[2])
    return wrapped(*cargs)


class FigureWrapper(object):
    """
    Class which assembles a variety of plotting convenience methods into a single usable package
    """

    def __init__(self, *args, **kwargs):
        defineSymbols()
        figure = kwargs.get('figure', None)
        if figure is None:
            figure = _plotting_convenience_.figure(*_convert_arguments_(args))
        self._figure = figure
        self._valid_groups = None

    @property
    def figure(self):
        """The underlying java Figure object"""
        return self._figure

    @property
    def widget(self):
        """The FigureWidget, if applicable. It will be `None` if .show() has NOT been called."""

        if _is_widget_(self.figure.getClass()):
            return self.figure
        return None

    @property
    def validGroups(self):
        """The collection, (actually java array), of valid users"""
        return _create_java_object_(self._valid_groups)

    @validGroups.setter
    def validGroups(self, groups):
        if groups is None:
            self._valid_groups = None
        elif _isStr(groups):
            self._valid_groups = [groups, ]
        else:
            try:
                self._valid_groups = list(groups)  # any other iterable will become a list
            except Exception as e:
                logging.error("Failed to set validGroups using input {} with exception {}".format(groups, e))

    def show(self):
        """
        Wraps the figure in a figure widget for display
        :return: FigureWrapper with figure attribute set to applicable widget
        """

        return FigureWrapper(figure=self._figure.show())

    def getWidget(self):
        """
        Get figure widget, if applicable. It will be `None` if .show() has NOT been called.
        :return: None or the widget reference
        """

        return self.widget

    def getValidGroups(self):
        """
        Get the collection of valid users
        :return: java array of user id strings
        """

        return self.validGroups

    def setValidGroups(self, groups):
        """
        Set the list of user ids which should have access to this figure wrapper object
        :param groups: None, single user id string, or list of user id strings
        """

        self.validGroups = groups

    @_convertArguments
    def axes(self, *args):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :param name: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) selected axes.
          
        *Overload 2*  
          :param id: int
          :return: (com.illumon.iris.db.plot.Figure) selected axes.
        """
        
        return FigureWrapper(figure=self.figure.axes(*args))

    @_convertArguments
    def axesRemoveSeries(self, *names):
        """
        Description copied from interface: Axes
        
        :param names: java.lang.String...
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.axesRemoveSeries(*names))

    @_convertArguments
    def axis(self, dim):
        """
        Description copied from interface: Axes
        
        :param dim: int
        :return: (com.illumon.iris.db.plot.Figure) Axis at dimension dim
        """
        
        return FigureWrapper(figure=self.figure.axis(dim))

    @_convertArguments
    def axisColor(self, color):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.axisColor(color))

    @_convertArguments
    def axisFormat(self, format):
        """
        Description copied from interface: Axis
        
        :param format: com.illumon.iris.db.plot.axisformatters.AxisFormat
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.axisFormat(format))

    @_convertArguments
    def axisFormatPattern(self, pattern):
        """
        Description copied from interface: Axis
        
        :param pattern: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.axisFormatPattern(pattern))

    @_convertArguments
    def axisLabel(self, label):
        """
        Description copied from interface: Axis
        
        :param label: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.axisLabel(label))

    @_convertArguments
    def axisLabelFont(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.axisLabelFont(*args))

    @_convertArguments
    def businessTime(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param calendar: com.illumon.util.calendar.BusinessCalendar
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.businessTime(*args))

    @_convertCatPlotArguments
    def catErrorBar(self, *args):
        """
        Description copied from interface: Axes
        
        There are 18 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: T1[]
          :param yLow: T2[]
          :param yHigh: T3[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: double[]
          :param yLow: double[]
          :param yHigh: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: float[]
          :param yLow: float[]
          :param yHigh: float[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 4*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: int[]
          :param yLow: int[]
          :param yHigh: int[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
        """
        
        return FigureWrapper(figure=self.figure.catErrorBar(*args))

    @_convertArguments
    def catErrorBarBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param categories: java.lang.String
          :param values: java.lang.String
          :param yLow: java.lang.String
          :param yHigh: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param categories: java.lang.String
          :param values: java.lang.String
          :param yLow: java.lang.String
          :param yHigh: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.catErrorBarBy(*args))

    @_convertArguments
    def catHistPlot(self, *args):
        """
        Description copied from interface: Axes
        
        There are 8 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param x: T[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param x: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 3*  
          :param seriesName: java.lang.Comparable
          :param x: float[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 4*  
          :param seriesName: java.lang.Comparable
          :param x: int[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.catHistPlot(*args))

    @_convertCatPlotArguments
    def catPlot(self, *args):
        """
        Description copied from interface: Axes
        
        There are 21 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: T1[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: float[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 4*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: int[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.catPlot(*args))

    @_convertCatPlot3dArguments
    def catPlot3d(self, *args):
        """
        Description copied from interface: Axes
        
        There are 38 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable,T2 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param xCategories: T0[]
          :param zCategories: T1[]
          :param values: T2[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param xCategories: T0[]
          :param zCategories: T1[]
          :param values: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param xCategories: T0[]
          :param zCategories: T1[]
          :param values: float[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 4*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param xCategories: T0[]
          :param zCategories: T1[]
          :param values: int[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.catPlot3d(*args))

    @_convertArguments
    def catPlot3dBy(self, seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns):
        """
        Description copied from interface: Axes
        
        :param seriesName: java.lang.Comparable
        :param t: com.illumon.iris.db.tables.Table
        :param xCategoriesColumn: java.lang.String
        :param zCategoriesColumn: java.lang.String
        :param valuesColumn: java.lang.String
        :param byColumns: java.lang.String...
        :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.catPlot3dBy(seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns))

    @_convertArguments
    def catPlotBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param categories: java.lang.String
          :param values: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param categories: java.lang.String
          :param values: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.catPlotBy(*args))

    @_convertArguments
    def chart(self, *args):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :param index: int
          :return: (com.illumon.iris.db.plot.Figure) selected Chart
          
        *Overload 2*  
          :param rowNum: int
          :param colNum: int
          :return: (com.illumon.iris.db.plot.Figure) selected Chart
        """
        
        return FigureWrapper(figure=self.figure.chart(*args))

    @_convertArguments
    def chartRemoveSeries(self, *names):
        """
        Description copied from interface: Chart
        
        :param names: java.lang.String...
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.chartRemoveSeries(*names))

    @_convertArguments
    def chartTitle(self, *args):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :param title: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param titleColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 3*  
          :param t: com.illumon.iris.db.tables.Table
          :param titleColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 4*  
          :param showColumnNamesInTitle: boolean
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param titleColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 5*  
          :param showColumnNamesInTitle: boolean
          :param t: com.illumon.iris.db.tables.Table
          :param titleColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 6*  
          :param titleFormat: java.lang.String
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param titleColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 7*  
          :param titleFormat: java.lang.String
          :param t: com.illumon.iris.db.tables.Table
          :param titleColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.chartTitle(*args))

    @_convertArguments
    def chartTitleColor(self, color):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.chartTitleColor(color))

    @_convertArguments
    def chartTitleFont(self, *args):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.chartTitleFont(*args))

    @_convertArguments
    def colSpan(self, n):
        """
        Description copied from interface: Chart
        
        :param n: int
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.colSpan(n))

    @_convertArguments
    def errorBarColor(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this DataSeries
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param color: int
          :return: (com.illumon.iris.db.plot.Figure) this DataSeries
          
        *Overload 4*  
          :param color: int
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 5*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this DataSeries
          
        *Overload 6*  
          :param color: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.errorBarColor(*args))

    @_convertArguments
    def errorBarX(self, *args):
        """
        Description copied from interface: Axes
        
        There are 39 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param xLow: T1[]
          :param xHigh: T2[]
          :param y: T3[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param xLow: T1[]
          :param xHigh: T2[]
          :param y: com.illumon.iris.db.tables.utils.DBDateTime[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param xLow: T1[]
          :param xHigh: T2[]
          :param y: java.util.Date[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 4*  
          :param seriesName: java.lang.Comparable
          :param x: double[]
          :param xLow: double[]
          :param xHigh: double[]
          :param y: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
        """
        
        return FigureWrapper(figure=self.figure.errorBarX(*args))

    @_convertArguments
    def errorBarXBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param x: java.lang.String
          :param xLow: java.lang.String
          :param xHigh: java.lang.String
          :param y: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param x: java.lang.String
          :param xLow: java.lang.String
          :param xHigh: java.lang.String
          :param y: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.errorBarXBy(*args))

    @_convertArguments
    def errorBarXY(self, *args):
        """
        Description copied from interface: Axes
        
        There are 39 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number,T4 extends java.lang.Number,T5 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param xLow: T1[]
          :param xHigh: T2[]
          :param y: T3[]
          :param yLow: T4[]
          :param yHigh: T5[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param xLow: T1[]
          :param xHigh: T2[]
          :param y: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param yLow: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param yHigh: com.illumon.iris.db.tables.utils.DBDateTime[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param xLow: T1[]
          :param xHigh: T2[]
          :param y: java.util.Date[]
          :param yLow: java.util.Date[]
          :param yHigh: java.util.Date[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 4*  
          :param seriesName: java.lang.Comparable
          :param x: double[]
          :param xLow: double[]
          :param xHigh: double[]
          :param y: double[]
          :param yLow: double[]
          :param yHigh: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
        """
        
        return FigureWrapper(figure=self.figure.errorBarXY(*args))

    @_convertArguments
    def errorBarXYBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param x: java.lang.String
          :param xLow: java.lang.String
          :param xHigh: java.lang.String
          :param y: java.lang.String
          :param yLow: java.lang.String
          :param yHigh: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param x: java.lang.String
          :param xLow: java.lang.String
          :param xHigh: java.lang.String
          :param y: java.lang.String
          :param yLow: java.lang.String
          :param yHigh: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.errorBarXYBy(*args))

    @_convertArguments
    def errorBarY(self, *args):
        """
        Description copied from interface: Axes
        
        There are 39 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: T1[]
          :param yLow: T2[]
          :param yHigh: T3[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param yLow: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param yHigh: com.illumon.iris.db.tables.utils.DBDateTime[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: java.util.Date[]
          :param yLow: java.util.Date[]
          :param yHigh: java.util.Date[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 4*  
          :param seriesName: java.lang.Comparable
          :param x: double[]
          :param y: double[]
          :param yLow: double[]
          :param yHigh: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
        """
        
        return FigureWrapper(figure=self.figure.errorBarY(*args))

    @_convertArguments
    def errorBarYBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param x: java.lang.String
          :param y: java.lang.String
          :param yLow: java.lang.String
          :param yHigh: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param x: java.lang.String
          :param y: java.lang.String
          :param yLow: java.lang.String
          :param yHigh: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.errorBarYBy(*args))

    @_convertArguments
    def figureRemoveSeries(self, *names):
        """
        Description copied from interface: BaseFigure
        
        :param names: java.lang.String...
        :return: (com.illumon.iris.db.plot.Figure) this Figure
        """
        
        return FigureWrapper(figure=self.figure.figureRemoveSeries(*names))

    @_convertArguments
    def figureTitle(self, title):
        """
        Description copied from interface: BaseFigure
        
        :param title: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Figure
        """
        
        return FigureWrapper(figure=self.figure.figureTitle(title))

    @_convertArguments
    def figureTitleColor(self, color):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Figure
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Figure
        """
        
        return FigureWrapper(figure=self.figure.figureTitleColor(color))

    @_convertArguments
    def figureTitleFont(self, *args):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Figure
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Figure
        """
        
        return FigureWrapper(figure=self.figure.figureTitleFont(*args))

    @_convertArguments
    def funcNPoints(self, npoints):
        """
        Description copied from interface: XYDataSeriesFunction
        
        :param npoints: int
        :return: (com.illumon.iris.db.plot.Figure) this dataset with the specified number of points.
        """
        
        return FigureWrapper(figure=self.figure.funcNPoints(npoints))

    @_convertArguments
    def funcRange(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: XYDataSeriesFunction
        
        *Overload 1*  
          :param xmin: double
          :param xmax: double
          :return: (com.illumon.iris.db.plot.Figure) this dataset with the new range
          
        *Overload 2*  
          :param xmin: double
          :param xmax: double
          :param zmin: double
          :param zmax: double
          :return: (com.illumon.iris.db.plot.Figure) this dataset with the new range
          
        *Overload 3*  
          :param xmin: double
          :param xmax: double
          :param zmin: double
          :param zmax: double
          :param npoints: int
          :return: (com.illumon.iris.db.plot.Figure) this dataset with the new range
          
        *Overload 4*  
          :param xmin: double
          :param xmax: double
          :param npoints: int
          :return: (com.illumon.iris.db.plot.Figure) this dataset with the new range
        """
        
        return FigureWrapper(figure=self.figure.funcRange(*args))

    @_convertArguments
    def gradientVisible(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param visible: boolean
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param visible: boolean
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.gradientVisible(*args))

    @_convertArguments
    def gridLinesVisible(self, visible):
        """
        Description copied from interface: Chart
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.gridLinesVisible(visible))

    @_convertArguments
    def group(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: CategoryDataSeries
        
        *Overload 1*  
          :param group: int
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param group: int
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.group(*args))

    @_convertArguments
    def histPlot(self, *args):
        """
        Description copied from interface: Axes
        
        There are 19 overloads, restricting signature summary to first 4:
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param counts: com.illumon.iris.db.tables.Table
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param nbins: int
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 3*  
          :param seriesName: java.lang.Comparable
          :param x: double[]
          :param nbins: int
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 4*  
          :param seriesName: java.lang.Comparable
          :param x: float[]
          :param nbins: int
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
        """
        
        return FigureWrapper(figure=self.figure.histPlot(*args))

    @_convertArguments
    def invert(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param invert: boolean
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.invert(*args))

    @_convertArguments
    def legendColor(self, color):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.legendColor(color))

    @_convertArguments
    def legendFont(self, *args):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Chart
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.legendFont(*args))

    @_convertArguments
    def legendVisible(self, visible):
        """
        Description copied from interface: Chart
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.legendVisible(visible))

    @_convertArguments
    def lineColor(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param color: int
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 4*  
          :param color: int
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 5*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 6*  
          :param color: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.lineColor(*args))

    @_convertArguments
    def lineStyle(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param style: com.illumon.iris.db.plot.LineStyle
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param style: com.illumon.iris.db.plot.LineStyle
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.lineStyle(*args))

    @_convertArguments
    def linesVisible(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param visible: java.lang.Boolean
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param visible: java.lang.Boolean
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.linesVisible(*args))

    @_convertArguments
    def log(self):
        """
        Description copied from interface: Axis
        
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.log())

    @_convertArguments
    def max(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :param max: double
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.max(*args))

    @_convertArguments
    def maxRowsInTitle(self, maxRowsCount):
        """
        Description copied from interface: Chart
        
        :param maxRowsCount: int
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.maxRowsInTitle(maxRowsCount))

    @_convertArguments
    def min(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :param min: double
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.min(*args))

    @_convertArguments
    def minorTicks(self, count):
        """
        Description copied from interface: Axis
        
        :param count: int
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.minorTicks(count))

    @_convertArguments
    def minorTicksVisible(self, visible):
        """
        Description copied from interface: Axis
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.minorTicksVisible(visible))

    @_convertArguments
    def newAxes(self, *args):
        """
        Description copied from interface: Chart
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) newly created Axes on this Chart
          
        *Overload 2*  
          :param name: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) newly created Axes on this Chart
          
        *Overload 3*  
          :param dim: int
          :return: (com.illumon.iris.db.plot.Figure) newly created Axes on this Chart
          
        *Overload 4*  
          :param name: java.lang.String
          :param dim: int
          :return: (com.illumon.iris.db.plot.Figure) newly created Axes on this Chart
        """
        
        return FigureWrapper(figure=self.figure.newAxes(*args))

    @_convertArguments
    def newChart(self, *args):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) the new Chart
          
        *Overload 2*  
          :param index: int
          :return: (com.illumon.iris.db.plot.Figure) the new Chart
          
        *Overload 3*  
          :param rowNum: int
          :param colNum: int
          :return: (com.illumon.iris.db.plot.Figure) the new Chart
        """
        
        return FigureWrapper(figure=self.figure.newChart(*args))

    @_convertArguments
    def ohlcPlot(self, *args):
        """
        Description copied from interface: Axes
        
        There are 17 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number,T4 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param open: T1[]
          :param high: T2[]
          :param low: T3[]
          :param close: T4[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param open: double[]
          :param high: double[]
          :param low: double[]
          :param close: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 3*  
          :param seriesName: java.lang.Comparable
          :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param open: float[]
          :param high: float[]
          :param low: float[]
          :param close: float[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
          
        *Overload 4*  
          :param seriesName: java.lang.Comparable
          :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
          :param open: int[]
          :param high: int[]
          :param low: int[]
          :param close: int[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created by the plot
        """
        
        return FigureWrapper(figure=self.figure.ohlcPlot(*args))

    @_convertArguments
    def ohlcPlotBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param timeCol: java.lang.String
          :param openCol: java.lang.String
          :param highCol: java.lang.String
          :param lowCol: java.lang.String
          :param closeCol: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param timeCol: java.lang.String
          :param openCol: java.lang.String
          :param highCol: java.lang.String
          :param lowCol: java.lang.String
          :param closeCol: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.ohlcPlotBy(*args))

    @_convertArguments
    def piePercentLabelFormat(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: CategoryDataSeries
        
        *Overload 1*  
          :param format: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param format: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.piePercentLabelFormat(*args))

    @_convertCatPlotArguments
    def piePlot(self, *args):
        """
        Description copied from interface: Axes
        
        There are 17 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: T1[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: float[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 4*  
          Note: Java generics information - <T0 extends java.lang.Comparable>
          
          :param seriesName: java.lang.Comparable
          :param categories: T0[]
          :param values: int[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.piePlot(*args))

    @_convertArguments
    def plot(self, *args):
        """
        Description copied from interface: Axes
        
        There are 86 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param function: groovy.lang.Closure<T>
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param function: java.util.function.DoubleUnaryOperator
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: T1[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 4*  
          Note: Java generics information - <T0 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.plot(*args))

    @_convertArguments
    def plot3d(self, *args):
        """
        Description copied from interface: Axes
        
        There are 733 overloads, restricting signature summary to first 4:
        *Overload 1*  
          Note: Java generics information - <T extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param function: groovy.lang.Closure<T>
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param function: java.util.function.DoubleBinaryOperator
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 3*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: T1[]
          :param z: T2[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 4*  
          Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number>
          
          :param seriesName: java.lang.Comparable
          :param x: T0[]
          :param y: T1[]
          :param z: double[]
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.plot3d(*args))

    @_convertArguments
    def plot3dBy(self, seriesName, t, x, y, z, *byColumns):
        """
        Description copied from interface: Axes
        
        :param seriesName: java.lang.Comparable
        :param t: com.illumon.iris.db.tables.Table
        :param x: java.lang.String
        :param y: java.lang.String
        :param z: java.lang.String
        :param byColumns: java.lang.String...
        :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.plot3dBy(seriesName, t, x, y, z, *byColumns))

    @_convertArguments
    def plotBy(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param seriesName: java.lang.Comparable
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param x: java.lang.String
          :param y: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
          
        *Overload 2*  
          :param seriesName: java.lang.Comparable
          :param t: com.illumon.iris.db.tables.Table
          :param x: java.lang.String
          :param y: java.lang.String
          :param byColumns: java.lang.String...
          :return: (com.illumon.iris.db.plot.Figure) dataset created for plot
        """
        
        return FigureWrapper(figure=self.figure.plotBy(*args))

    @_convertArguments
    def plotOrientation(self, orientation):
        """
        Description copied from interface: Chart
        
        :param orientation: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.plotOrientation(orientation))

    @_convertArguments
    def plotStyle(self, style):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param style: com.illumon.iris.db.plot.PlotStyle
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param style: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.plotStyle(style))

    @_convertArguments
    def pointColor(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: XYDataSeries
        
        There are 48 overloads, restricting signature summary to first 4:
        *Overload 1*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param keyColumn: java.lang.String
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries
          
        *Overload 4*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param keyColumn: java.lang.String
          :param valueColumn: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColor(*args))

    @_convertArguments
    def pointColorByX(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: CategoryDataSeries3D
        
        *Overload 1*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: groovy.lang.Closure<COLOR>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 2*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: groovy.lang.Closure<COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 4*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColorByX(*args))

    @_convertArguments
    def pointColorByY(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          Note: Java generics information - <T extends com.illumon.iris.gui.color.Paint>
          
          :param colors: groovy.lang.Closure<T>
          :return: (com.illumon.iris.db.plot.Figure) this DataSeries
          
        *Overload 2*  
          Note: Java generics information - <T extends com.illumon.iris.gui.color.Paint>
          
          :param colors: groovy.lang.Closure<T>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <T extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.Map<java.lang.Double,T>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries
          
        *Overload 4*  
          Note: Java generics information - <T extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.Map<java.lang.Double,T>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 5*  
          Note: Java generics information - <T extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.function.Function<java.lang.Double,T>
          :return: (com.illumon.iris.db.plot.Figure) this DataSeries
          
        *Overload 6*  
          Note: Java generics information - <T extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.function.Function<java.lang.Double,T>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColorByY(*args))

    @_convertArguments
    def pointColorByZ(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: CategoryDataSeries3D
        
        *Overload 1*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: groovy.lang.Closure<COLOR>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 2*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: groovy.lang.Closure<COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 4*  
          Note: Java generics information - <COLOR extends com.illumon.iris.gui.color.Paint>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColorByZ(*args))

    @_convertArguments
    def pointColorInteger(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: XYDataSeries
        
        There are 10 overloads, restricting signature summary to first 4:
        *Overload 1*  
          :param colors: com.illumon.iris.db.plot.datasets.data.IndexableData<java.lang.Integer>
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 2*  
          :param colors: com.illumon.iris.db.plot.datasets.data.IndexableData<java.lang.Integer>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <CATEGORY extends java.lang.Comparable,COLOR extends java.lang.Integer>
          
          :param colors: java.util.Map<CATEGORY,COLOR>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries
          
        *Overload 4*  
          Note: Java generics information - <CATEGORY extends java.lang.Comparable,COLOR extends java.lang.Integer>
          
          :param colors: java.util.Map<CATEGORY,COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColorInteger(*args))

    @_convertArguments
    def pointColorIntegerByX(self, *args):
        """
        *Overload 1*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: groovy.lang.Closure<COLOR>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 2*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: groovy.lang.Closure<COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 4*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColorIntegerByX(*args))

    @_convertArguments
    def pointColorIntegerByZ(self, *args):
        """
        *Overload 1*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: groovy.lang.Closure<COLOR>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 2*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: groovy.lang.Closure<COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 4*  
          Note: Java generics information - <COLOR extends java.lang.Integer>
          
          :param colors: java.util.function.Function<java.lang.Comparable,COLOR>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointColorIntegerByZ(*args))

    @_convertArguments
    def pointLabel(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: XYDataSeries
        
        There are 30 overloads, restricting signature summary to first 4:
        *Overload 1*  
          :param labels: com.illumon.iris.db.plot.datasets.data.IndexableData<?>
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 2*  
          :param labels: com.illumon.iris.db.plot.datasets.data.IndexableData<?>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 4*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointLabel(*args))

    @_convertArguments
    def pointLabelByX(self, *args):
        """
        *Overload 1*  
          Note: Java generics information - <LABEL>
          
          :param labels: groovy.lang.Closure<LABEL>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 2*  
          Note: Java generics information - <LABEL>
          
          :param labels: groovy.lang.Closure<LABEL>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <LABEL>
          
          :param labels: java.util.function.Function<java.lang.Comparable,LABEL>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 4*  
          Note: Java generics information - <LABEL>
          
          :param labels: java.util.function.Function<java.lang.Comparable,LABEL>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointLabelByX(*args))

    @_convertArguments
    def pointLabelByZ(self, *args):
        """
        *Overload 1*  
          Note: Java generics information - <LABEL>
          
          :param labels: groovy.lang.Closure<LABEL>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 2*  
          Note: Java generics information - <LABEL>
          
          :param labels: groovy.lang.Closure<LABEL>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <LABEL>
          
          :param labels: java.util.function.Function<java.lang.Comparable,LABEL>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 4*  
          Note: Java generics information - <LABEL>
          
          :param labels: java.util.function.Function<java.lang.Comparable,LABEL>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointLabelByZ(*args))

    @_convertArguments
    def pointLabelFormat(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param format: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param format: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointLabelFormat(*args))

    @_convertArguments
    def pointShape(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: XYDataSeries
        
        There are 28 overloads, restricting signature summary to first 4:
        *Overload 1*  
          :param shapes: com.illumon.iris.db.plot.datasets.data.IndexableData<java.lang.String>
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 2*  
          :param shapes: com.illumon.iris.db.plot.datasets.data.IndexableData<java.lang.String>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 4*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointShape(*args))

    @_convertArguments
    def pointSize(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: XYDataSeries
        
        There are 70 overloads, restricting signature summary to first 4:
        *Overload 1*  
          :param factors: com.illumon.iris.db.plot.datasets.data.IndexableData<java.lang.Double>
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 2*  
          :param factors: com.illumon.iris.db.plot.datasets.data.IndexableData<java.lang.Double>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this XYDataSeries
          
        *Overload 4*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param columnName: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointSize(*args))

    @_convertArguments
    def pointSizeByX(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: CategoryDataSeries3D
        
        *Overload 1*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: groovy.lang.Closure<NUMBER>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 2*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: groovy.lang.Closure<NUMBER>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: java.util.function.Function<java.lang.Comparable,NUMBER>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 4*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: java.util.function.Function<java.lang.Comparable,NUMBER>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointSizeByX(*args))

    @_convertArguments
    def pointSizeByZ(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: CategoryDataSeries3D
        
        *Overload 1*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: groovy.lang.Closure<NUMBER>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 2*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: groovy.lang.Closure<NUMBER>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: java.util.function.Function<java.lang.Comparable,NUMBER>
          :return: (com.illumon.iris.db.plot.Figure) this CategoryDataSeries3D
          
        *Overload 4*  
          Note: Java generics information - <NUMBER extends java.lang.Number>
          
          :param factors: java.util.function.Function<java.lang.Comparable,NUMBER>
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointSizeByZ(*args))

    @_convertArguments
    def pointsVisible(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param visible: java.lang.Boolean
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param visible: java.lang.Boolean
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.pointsVisible(*args))

    @_convertArguments
    def range(self, min, max):
        """
        Description copied from interface: Axis
        
        :param min: double
        :param max: double
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.range(min, max))

    @_convertArguments
    def removeChart(self, *args):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :param index: int
          :return: (com.illumon.iris.db.plot.Figure) this Figure
          
        *Overload 2*  
          :param rowNum: int
          :param colNum: int
          :return: (com.illumon.iris.db.plot.Figure) the new Chart
        """
        
        return FigureWrapper(figure=self.figure.removeChart(*args))

    @_convertArguments
    def rowSpan(self, n):
        """
        Description copied from interface: Chart
        
        :param n: int
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.rowSpan(n))

    @_convertArguments
    def save(self, *args):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :param saveLocation: java.lang.String
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 2*  
          :param saveLocation: java.lang.String
          :param width: int
          :param height: int
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param saveLocation: java.lang.String
          :param wait: boolean
          :param timeoutSeconds: long
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 4*  
          :param saveLocation: java.lang.String
          :param width: int
          :param height: int
          :param wait: boolean
          :param timeoutSeconds: long
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.save(*args))

    @_convertArguments
    def series(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param id: int
          :return: (com.illumon.iris.db.plot.Figure) selected data series.
          
        *Overload 2*  
          :param name: java.lang.Comparable
          :return: (com.illumon.iris.db.plot.Figure) selected data series.
        """
        
        return FigureWrapper(figure=self.figure.series(*args))

    @_convertArguments
    def seriesColor(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 3*  
          :param color: int
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 4*  
          :param color: int
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 5*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 6*  
          :param color: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.seriesColor(*args))

    @_convertArguments
    def seriesNamingFunction(self, namingFunction):
        """
        Description copied from interface: MultiSeries
        
        *Overload 1*  
          :param namingFunction: groovy.lang.Closure<java.lang.String>
          :return: com.illumon.iris.db.plot.Figure
          
        *Overload 2*  
          :param namingFunction: java.util.function.Function<java.lang.Object,java.lang.String>
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.seriesNamingFunction(namingFunction))

    @_convertArguments
    def span(self, rowSpan, colSpan):
        """
        Description copied from interface: Chart
        
        :param rowSpan: int
        :param colSpan: int
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.span(rowSpan, colSpan))

    @_convertArguments
    def theme(self, theme):
        """
        Description copied from interface: BaseFigure
        
        *Overload 1*  
          :param theme: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Figure
          
        *Overload 2*  
          :param theme: com.illumon.iris.db.plot.Theme
          :return: (com.illumon.iris.db.plot.Figure) this Figure
        """
        
        return FigureWrapper(figure=self.figure.theme(theme))

    @_convertArguments
    def tickLabelAngle(self, angle):
        """
        Description copied from interface: Axis
        
        :param angle: double
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.tickLabelAngle(angle))

    @_convertArguments
    def ticks(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :param tickLocations: double[]
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param gapBetweenTicks: double
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.ticks(*args))

    @_convertArguments
    def ticksFont(self, *args):
        """
        Description copied from interface: Axis
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.ticksFont(*args))

    @_convertArguments
    def ticksVisible(self, visible):
        """
        Description copied from interface: Axis
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.ticksVisible(visible))

    @_convertArguments
    def toolTipPattern(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param format: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param format: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.toolTipPattern(*args))

    @_convertArguments
    def transform(self, transform):
        """
        Description copied from interface: Axis
        
        :param transform: com.illumon.iris.db.plot.axistransformations.AxisTransform
        :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.transform(transform))

    @_convertArguments
    def twin(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
          
        *Overload 2*  
          :param name: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
          
        *Overload 3*  
          :param dim: int
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
          
        *Overload 4*  
          :param name: java.lang.String
          :param dim: int
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
        """
        
        return FigureWrapper(figure=self.figure.twin(*args))

    @_convertArguments
    def twinX(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
          
        *Overload 2*  
          :param name: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
        """
        
        return FigureWrapper(figure=self.figure.twinX(*args))

    @_convertArguments
    def twinY(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
          
        *Overload 2*  
          :param name: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
        """
        
        return FigureWrapper(figure=self.figure.twinY(*args))

    @_convertArguments
    def twinZ(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
          
        *Overload 2*  
          :param name: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) the new Axes instance
        """
        
        return FigureWrapper(figure=self.figure.twinZ(*args))

    @_convertArguments
    def updateInterval(self, updateIntervalMillis):
        """
        Description copied from interface: BaseFigure
        
        :param updateIntervalMillis: long
        :return: (com.illumon.iris.db.plot.Figure) this Figure
        """
        
        return FigureWrapper(figure=self.figure.updateInterval(updateIntervalMillis))

    @_convertArguments
    def xAxis(self):
        """
        Description copied from interface: Axes
        
        :return: (com.illumon.iris.db.plot.Figure) x-dimension Axis
        """
        
        return FigureWrapper(figure=self.figure.xAxis())

    @_convertArguments
    def xBusinessTime(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param calendar: com.illumon.util.calendar.BusinessCalendar
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xBusinessTime(*args))

    @_convertArguments
    def xColor(self, color):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xColor(color))

    @_convertArguments
    def xFormat(self, format):
        """
        Description copied from interface: Axes
        
        :param format: com.illumon.iris.db.plot.axisformatters.AxisFormat
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xFormat(format))

    @_convertArguments
    def xFormatPattern(self, pattern):
        """
        Description copied from interface: Axes
        
        :param pattern: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xFormatPattern(pattern))

    @_convertArguments
    def xGridLinesVisible(self, visible):
        """
        Description copied from interface: Chart
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.xGridLinesVisible(visible))

    @_convertArguments
    def xInvert(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param invert: boolean
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xInvert(*args))

    @_convertArguments
    def xLabel(self, label):
        """
        Description copied from interface: Axes
        
        :param label: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xLabel(label))

    @_convertArguments
    def xLabelFont(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.xLabelFont(*args))

    @_convertArguments
    def xLog(self):
        """
        Description copied from interface: Axes
        
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xLog())

    @_convertArguments
    def xMax(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param max: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xMax(*args))

    @_convertArguments
    def xMin(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param min: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xMin(*args))

    @_convertArguments
    def xMinorTicks(self, count):
        """
        Description copied from interface: Axes
        
        :param count: int
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xMinorTicks(count))

    @_convertArguments
    def xMinorTicksVisible(self, visible):
        """
        Description copied from interface: Axes
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xMinorTicksVisible(visible))

    @_convertArguments
    def xRange(self, min, max):
        """
        Description copied from interface: Axes
        
        :param min: double
        :param max: double
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xRange(min, max))

    @_convertArguments
    def xTickLabelAngle(self, angle):
        """
        Description copied from interface: Axes
        
        :param angle: double
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xTickLabelAngle(angle))

    @_convertArguments
    def xTicks(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param tickLocations: double[]
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param gapBetweenTicks: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xTicks(*args))

    @_convertArguments
    def xTicksFont(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.xTicksFont(*args))

    @_convertArguments
    def xTicksVisible(self, visible):
        """
        Description copied from interface: Axes
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xTicksVisible(visible))

    @_convertArguments
    def xToolTipPattern(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param format: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param format: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.xToolTipPattern(*args))

    @_convertArguments
    def xTransform(self, transform):
        """
        Description copied from interface: Axes
        
        :param transform: com.illumon.iris.db.plot.axistransformations.AxisTransform
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.xTransform(transform))

    @_convertArguments
    def yAxis(self):
        """
        Description copied from interface: Axes
        
        :return: (com.illumon.iris.db.plot.Figure) y-dimension Axis
        """
        
        return FigureWrapper(figure=self.figure.yAxis())

    @_convertArguments
    def yBusinessTime(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param calendar: com.illumon.util.calendar.BusinessCalendar
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yBusinessTime(*args))

    @_convertArguments
    def yColor(self, color):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yColor(color))

    @_convertArguments
    def yFormat(self, format):
        """
        Description copied from interface: Axes
        
        :param format: com.illumon.iris.db.plot.axisformatters.AxisFormat
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yFormat(format))

    @_convertArguments
    def yFormatPattern(self, pattern):
        """
        Description copied from interface: Axes
        
        :param pattern: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yFormatPattern(pattern))

    @_convertArguments
    def yGridLinesVisible(self, visible):
        """
        Description copied from interface: Chart
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Chart
        """
        
        return FigureWrapper(figure=self.figure.yGridLinesVisible(visible))

    @_convertArguments
    def yInvert(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param invert: boolean
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yInvert(*args))

    @_convertArguments
    def yLabel(self, label):
        """
        Description copied from interface: Axes
        
        :param label: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yLabel(label))

    @_convertArguments
    def yLabelFont(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.yLabelFont(*args))

    @_convertArguments
    def yLog(self):
        """
        Description copied from interface: Axes
        
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yLog())

    @_convertArguments
    def yMax(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param max: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yMax(*args))

    @_convertArguments
    def yMin(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param min: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yMin(*args))

    @_convertArguments
    def yMinorTicks(self, count):
        """
        Description copied from interface: Axes
        
        :param count: int
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yMinorTicks(count))

    @_convertArguments
    def yMinorTicksVisible(self, visible):
        """
        Description copied from interface: Axes
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yMinorTicksVisible(visible))

    @_convertArguments
    def yRange(self, min, max):
        """
        Description copied from interface: Axes
        
        :param min: double
        :param max: double
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yRange(min, max))

    @_convertArguments
    def yTickLabelAngle(self, angle):
        """
        Description copied from interface: Axes
        
        :param angle: double
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yTickLabelAngle(angle))

    @_convertArguments
    def yTicks(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param tickLocations: double[]
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param gapBetweenTicks: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yTicks(*args))

    @_convertArguments
    def yTicksFont(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.yTicksFont(*args))

    @_convertArguments
    def yTicksVisible(self, visible):
        """
        Description copied from interface: Axes
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yTicksVisible(visible))

    @_convertArguments
    def yToolTipPattern(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries
        
        *Overload 1*  
          :param format: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param format: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.yToolTipPattern(*args))

    @_convertArguments
    def yTransform(self, transform):
        """
        Description copied from interface: Axes
        
        :param transform: com.illumon.iris.db.plot.axistransformations.AxisTransform
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.yTransform(transform))

    @_convertArguments
    def zAxis(self):
        """
        Description copied from interface: Axes
        
        :return: (com.illumon.iris.db.plot.Figure) z-dimension Axis
        """
        
        return FigureWrapper(figure=self.figure.zAxis())

    @_convertArguments
    def zBusinessTime(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param calendar: com.illumon.util.calendar.BusinessCalendar
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 3*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zBusinessTime(*args))

    @_convertArguments
    def zColor(self, color):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param color: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param color: com.illumon.iris.gui.color.Paint
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zColor(color))

    @_convertArguments
    def zFormat(self, format):
        """
        Description copied from interface: Axes
        
        :param format: com.illumon.iris.db.plot.axisformatters.AxisFormat
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zFormat(format))

    @_convertArguments
    def zFormatPattern(self, pattern):
        """
        Description copied from interface: Axes
        
        :param pattern: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zFormatPattern(pattern))

    @_convertArguments
    def zInvert(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param invert: boolean
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zInvert(*args))

    @_convertArguments
    def zLabel(self, label):
        """
        Description copied from interface: Axes
        
        :param label: java.lang.String
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zLabel(label))

    @_convertArguments
    def zLabelFont(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.zLabelFont(*args))

    @_convertArguments
    def zLog(self):
        """
        Description copied from interface: Axes
        
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zLog())

    @_convertArguments
    def zMax(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param max: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zMax(*args))

    @_convertArguments
    def zMin(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param min: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
          :param valueColumn: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zMin(*args))

    @_convertArguments
    def zMinorTicks(self, count):
        """
        Description copied from interface: Axes
        
        :param count: int
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zMinorTicks(count))

    @_convertArguments
    def zMinorTicksVisible(self, visible):
        """
        Description copied from interface: Axes
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zMinorTicksVisible(visible))

    @_convertArguments
    def zRange(self, min, max):
        """
        Description copied from interface: Axes
        
        :param min: double
        :param max: double
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zRange(min, max))

    @_convertArguments
    def zTickLabelAngle(self, angle):
        """
        Description copied from interface: Axes
        
        :param angle: double
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zTickLabelAngle(angle))

    @_convertArguments
    def zTicks(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param tickLocations: double[]
          :return: (com.illumon.iris.db.plot.Figure) this Axes
          
        *Overload 2*  
          :param gapBetweenTicks: double
          :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zTicks(*args))

    @_convertArguments
    def zTicksFont(self, *args):
        """
        Description copied from interface: Axes
        
        *Overload 1*  
          :param font: com.illumon.iris.db.plot.Font
          :return: (com.illumon.iris.db.plot.Figure) this Axis
          
        *Overload 2*  
          :param family: java.lang.String
          :param style: java.lang.String
          :param size: int
          :return: (com.illumon.iris.db.plot.Figure) this Axis
        """
        
        return FigureWrapper(figure=self.figure.zTicksFont(*args))

    @_convertArguments
    def zTicksVisible(self, visible):
        """
        Description copied from interface: Axes
        
        :param visible: boolean
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zTicksVisible(visible))

    @_convertArguments
    def zToolTipPattern(self, *args):
        """
        **Incompatible overloads text - text from the first overload:**
        
        Description copied from interface: DataSeries3D
        
        *Overload 1*  
          :param format: java.lang.String
          :return: (com.illumon.iris.db.plot.Figure) this dataset
          
        *Overload 2*  
          :param format: java.lang.String
          :param keys: java.lang.Object...
          :return: com.illumon.iris.db.plot.Figure
        """
        
        return FigureWrapper(figure=self.figure.zToolTipPattern(*args))

    @_convertArguments
    def zTransform(self, transform):
        """
        Description copied from interface: Axes
        
        :param transform: com.illumon.iris.db.plot.axistransformations.AxisTransform
        :return: (com.illumon.iris.db.plot.Figure) this Axes
        """
        
        return FigureWrapper(figure=self.figure.zTransform(transform))
