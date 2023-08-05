#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

####################################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonFigureWrapper or
# "./gradlew :Generators:generatePythonFigureWrapper" to generate
####################################################################################


import jpy
import wrapt
from .figure_wrapper import FigureWrapper, _convert_arguments_


_plotting_convenience_ = None  # this module will be useless with no jvm


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _plotting_convenience_
    if _plotting_convenience_ is None:
        # an exception will be raised if not in the jvm classpath
        _plotting_convenience_ = jpy.get_type("com.illumon.iris.db.plot.PlottingConvenience")


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

    defineSymbols()
    return wrapped(*_convert_arguments_(args))


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


def figure(*args):
    return FigureWrapper(*args)


def catErrorBar(*args):
    """
    See Figure.catErrorBar(java.lang.Comparable, T0[], T1[], T2[], T3[])
    
    There are 18 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: T1[]
      :param yLow: T2[]
      :param yHigh: T3[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: double[]
      :param yLow: double[]
      :param yHigh: double[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: float[]
      :param yLow: float[]
      :param yHigh: float[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: int[]
      :param yLow: int[]
      :param yHigh: int[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catErrorBar(*args)


def catErrorBarBy(*args):
    """
    See Figure.catErrorBarBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
      :param categories: java.lang.String
      :param values: java.lang.String
      :param yLow: java.lang.String
      :param yHigh: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param t: com.illumon.iris.db.tables.Table
      :param categories: java.lang.String
      :param values: java.lang.String
      :param yLow: java.lang.String
      :param yHigh: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catErrorBarBy(*args)


def catHistPlot(*args):
    """
    See Figure.catHistPlot(java.lang.Comparable, T[])
    
    There are 8 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param x: T[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param x: double[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      :param seriesName: java.lang.Comparable
      :param x: float[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param seriesName: java.lang.Comparable
      :param x: int[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catHistPlot(*args)


def catPlot(*args):
    """
    See Figure.catPlot(java.lang.Comparable, T0[], T1[])
    
    There are 21 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: T1[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: double[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: float[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: int[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catPlot(*args)


def catPlot3d(*args):
    """
    See Figure.catPlot3d(java.lang.Comparable, T0[], T1[], T2[])
    
    There are 38 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable,T2 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param xCategories: T0[]
      :param zCategories: T1[]
      :param values: T2[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param xCategories: T0[]
      :param zCategories: T1[]
      :param values: double[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param xCategories: T0[]
      :param zCategories: T1[]
      :param values: float[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param xCategories: T0[]
      :param zCategories: T1[]
      :param values: int[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catPlot3d(*args)


def catPlot3dBy(seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns):
    """
    See Figure.catPlot3dBy(java.lang.Comparable, com.illumon.iris.db.tables.Table, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
    :param seriesName: java.lang.Comparable
    :param t: com.illumon.iris.db.tables.Table
    :param xCategoriesColumn: java.lang.String
    :param zCategoriesColumn: java.lang.String
    :param valuesColumn: java.lang.String
    :param byColumns: java.lang.String...
    :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catPlot3dBy(seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns)


def catPlotBy(*args):
    """
    See Figure.catPlotBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String...)
    
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
      :param categories: java.lang.String
      :param values: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param t: com.illumon.iris.db.tables.Table
      :param categories: java.lang.String
      :param values: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().catPlotBy(*args)


@_convertArguments
def color(color):
    """
    See Color.color
    
    :param color: java.lang.String
    :return: com.illumon.iris.gui.color.Color
    """
    
    return _plotting_convenience_.color(color)


@_convertArguments
def colorHSL(*args):
    """
    See Color.colorHSL(float, float, float)
    
    *Overload 1*  
      :param h: float
      :param s: float
      :param l: float
      :return: com.illumon.iris.gui.color.Color
      
    *Overload 2*  
      :param h: float
      :param s: float
      :param l: float
      :param a: float
      :return: com.illumon.iris.gui.color.Color
    """
    
    return _plotting_convenience_.colorHSL(*args)


@_convertArguments
def colorNames():
    """
    See Color.colorNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.colorNames())


@_convertArguments
def colorRGB(*args):
    """
    See Color.colorRGB(int, int, int)
    
    *Overload 1*  
      :param rgb: int
      :return: com.illumon.iris.gui.color.Color
      
    *Overload 2*  
      :param rgba: int
      :param hasAlpha: boolean
      :return: com.illumon.iris.gui.color.Color
      
    *Overload 3*  
      :param r: float
      :param g: float
      :param b: float
      :return: com.illumon.iris.gui.color.Color
      
    *Overload 4*  
      :param r: int
      :param g: int
      :param b: int
      :return: com.illumon.iris.gui.color.Color
      
    *Overload 5*  
      :param r: float
      :param g: float
      :param b: float
      :param a: float
      :return: com.illumon.iris.gui.color.Color
      
    *Overload 6*  
      :param r: int
      :param g: int
      :param b: int
      :param a: int
      :return: com.illumon.iris.gui.color.Color
    """
    
    return _plotting_convenience_.colorRGB(*args)


def errorBarX(*args):
    """
    See Figure.errorBarX(java.lang.Comparable, T0[], T1[], T2[], T3[])
    
    There are 39 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param xLow: T1[]
      :param xHigh: T2[]
      :param y: T3[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param xLow: T1[]
      :param xHigh: T2[]
      :param y: com.illumon.iris.db.tables.utils.DBDateTime[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param xLow: T1[]
      :param xHigh: T2[]
      :param y: java.util.Date[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param seriesName: java.lang.Comparable
      :param x: double[]
      :param xLow: double[]
      :param xHigh: double[]
      :param y: double[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().errorBarX(*args)


def errorBarXBy(*args):
    """
    See Figure.errorBarXBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
      :param x: java.lang.String
      :param xLow: java.lang.String
      :param xHigh: java.lang.String
      :param y: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param t: com.illumon.iris.db.tables.Table
      :param x: java.lang.String
      :param xLow: java.lang.String
      :param xHigh: java.lang.String
      :param y: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().errorBarXBy(*args)


def errorBarXY(*args):
    """
    See Figure.errorBarXY(java.lang.Comparable, T0[], T1[], T2[], T3[], T4[], T5[])
    
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
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param xLow: T1[]
      :param xHigh: T2[]
      :param y: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param yLow: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param yHigh: com.illumon.iris.db.tables.utils.DBDateTime[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param xLow: T1[]
      :param xHigh: T2[]
      :param y: java.util.Date[]
      :param yLow: java.util.Date[]
      :param yHigh: java.util.Date[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param seriesName: java.lang.Comparable
      :param x: double[]
      :param xLow: double[]
      :param xHigh: double[]
      :param y: double[]
      :param yLow: double[]
      :param yHigh: double[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().errorBarXY(*args)


def errorBarXYBy(*args):
    """
    See Figure.errorBarXYBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
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
      :return: com.illumon.iris.db.plot.Figure
      
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
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().errorBarXYBy(*args)


def errorBarY(*args):
    """
    See Figure.errorBarY(java.lang.Comparable, T0[], T1[], T2[], T3[])
    
    There are 39 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: T1[]
      :param yLow: T2[]
      :param yHigh: T3[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param yLow: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param yHigh: com.illumon.iris.db.tables.utils.DBDateTime[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: java.util.Date[]
      :param yLow: java.util.Date[]
      :param yHigh: java.util.Date[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param seriesName: java.lang.Comparable
      :param x: double[]
      :param y: double[]
      :param yLow: double[]
      :param yHigh: double[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().errorBarY(*args)


def errorBarYBy(*args):
    """
    See Figure.errorBarYBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
      :param x: java.lang.String
      :param y: java.lang.String
      :param yLow: java.lang.String
      :param yHigh: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param t: com.illumon.iris.db.tables.Table
      :param x: java.lang.String
      :param y: java.lang.String
      :param yLow: java.lang.String
      :param yHigh: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().errorBarYBy(*args)


@_convertArguments
def font(family, style, size):
    """
    See Font.font
    
    *Overload 1*  
      :param family: java.lang.String
      :param style: com.illumon.iris.db.plot.Font.FontStyle
      :param size: int
      :return: com.illumon.iris.db.plot.Font
      
    *Overload 2*  
      :param family: java.lang.String
      :param style: java.lang.String
      :param size: int
      :return: com.illumon.iris.db.plot.Font
    """
    
    return _plotting_convenience_.font(family, style, size)


@_convertArguments
def fontFamilyNames():
    """
    See Font.fontFamilyNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.fontFamilyNames())


@_convertArguments
def fontStyle(style):
    """
    See Font.fontStyle(java.lang.String)
    
    :param style: java.lang.String
    :return: com.illumon.iris.db.plot.Font.FontStyle
    """
    
    return _plotting_convenience_.fontStyle(style)


@_convertArguments
def fontStyleNames():
    """
    See Font.fontStyleNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.fontStyleNames())


def histPlot(*args):
    """
    See Figure.histPlot(java.lang.Comparable, com.illumon.iris.db.tables.Table)
    
    There are 19 overloads, restricting signature summary to first 4:
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param counts: com.illumon.iris.db.tables.Table
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param nbins: int
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      :param seriesName: java.lang.Comparable
      :param x: double[]
      :param nbins: int
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param seriesName: java.lang.Comparable
      :param x: float[]
      :param nbins: int
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().histPlot(*args)


@_convertArguments
def lineEndStyle(style):
    """
    See LineStyle.lineEndStyle(java.lang.String)
    
    :param style: java.lang.String
    :return: com.illumon.iris.db.plot.LineStyle.LineEndStyle
    """
    
    return _plotting_convenience_.lineEndStyle(style)


@_convertArguments
def lineEndStyleNames():
    """
    See LineStyle.lineEndStyleNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.lineEndStyleNames())


@_convertArguments
def lineJoinStyle(style):
    """
    See LineStyle.lineJoinStyle(java.lang.String)
    
    :param style: java.lang.String
    :return: com.illumon.iris.db.plot.LineStyle.LineJoinStyle
    """
    
    return _plotting_convenience_.lineJoinStyle(style)


@_convertArguments
def lineJoinStyleNames():
    """
    See LineStyle.lineJoinStyleNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.lineJoinStyleNames())


@_convertArguments
def lineStyle(*args):
    """
    See LineStyle.lineStyle(double, com.illumon.iris.db.plot.LineStyle.LineEndStyle, com.illumon.iris.db.plot.LineStyle.LineJoinStyle, double...)
    
    There are 15 overloads, restricting signature summary to first 4:
    *Overload 1*  
      :return: com.illumon.iris.db.plot.LineStyle
      
    *Overload 2*  
      :param dashPattern: double...
      :return: com.illumon.iris.db.plot.LineStyle
      
    *Overload 3*  
      :param width: double
      :return: com.illumon.iris.db.plot.LineStyle
      
    *Overload 4*  
      Note: Java generics information - <T extends java.lang.Number>
      
      :param dashPattern: java.util.List<T>
      :return: com.illumon.iris.db.plot.LineStyle
    """
    
    return _plotting_convenience_.lineStyle(*args)


def newAxes(*args):
    """
    See Figure.newAxes()
    
    *Overload 1*  
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param name: java.lang.String
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      :param dim: int
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param name: java.lang.String
      :param dim: int
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().newAxes(*args)


def newChart(*args):
    """
    See Figure.newChart()
    
    *Overload 1*  
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param index: int
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      :param rowNum: int
      :param colNum: int
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().newChart(*args)


def ohlcPlot(*args):
    """
    See Figure.ohlcPlot(java.lang.Comparable, com.illumon.iris.db.tables.utils.DBDateTime[], T1[], T2[], T3[], T4[])
    
    There are 17 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T1 extends java.lang.Number,T2 extends java.lang.Number,T3 extends java.lang.Number,T4 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param open: T1[]
      :param high: T2[]
      :param low: T3[]
      :param close: T4[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param open: double[]
      :param high: double[]
      :param low: double[]
      :param close: double[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      :param seriesName: java.lang.Comparable
      :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param open: float[]
      :param high: float[]
      :param low: float[]
      :param close: float[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      :param seriesName: java.lang.Comparable
      :param time: com.illumon.iris.db.tables.utils.DBDateTime[]
      :param open: int[]
      :param high: int[]
      :param low: int[]
      :param close: int[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().ohlcPlot(*args)


def ohlcPlotBy(*args):
    """
    See Figure.ohlcPlotBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
      :param timeCol: java.lang.String
      :param openCol: java.lang.String
      :param highCol: java.lang.String
      :param lowCol: java.lang.String
      :param closeCol: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param t: com.illumon.iris.db.tables.Table
      :param timeCol: java.lang.String
      :param openCol: java.lang.String
      :param highCol: java.lang.String
      :param lowCol: java.lang.String
      :param closeCol: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().ohlcPlotBy(*args)


@_convertArguments
def oneClick(*args):
    """
    See Selectables.oneClick(com.illumon.iris.db.tables.Table, java.lang.String...)
    
    *Overload 1*  
      :param t: com.illumon.iris.db.tables.Table
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.filters.SelectableDataSetOneClick
      
    *Overload 2*  
      :param t: com.illumon.iris.db.tables.Table
      :param requireAllFiltersToDisplay: boolean
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.filters.SelectableDataSetOneClick
      
    *Overload 3*  
      :param tMap: com.illumon.iris.db.v2.TableMap
      :param tableDefinition: com.illumon.iris.db.tables.TableDefinition
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.filters.SelectableDataSetOneClick
      
    *Overload 4*  
      :param tMap: com.illumon.iris.db.v2.TableMap
      :param t: com.illumon.iris.db.tables.Table
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.filters.SelectableDataSetOneClick
      
    *Overload 5*  
      :param tMap: com.illumon.iris.db.v2.TableMap
      :param tableDefinition: com.illumon.iris.db.tables.TableDefinition
      :param requireAllFiltersToDisplay: boolean
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.filters.SelectableDataSetOneClick
      
    *Overload 6*  
      :param tMap: com.illumon.iris.db.v2.TableMap
      :param t: com.illumon.iris.db.tables.Table
      :param requireAllFiltersToDisplay: boolean
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.filters.SelectableDataSetOneClick
    """
    
    return _plotting_convenience_.oneClick(*args)


def piePlot(*args):
    """
    See Figure.piePlot(java.lang.Comparable, T0[], T1[])
    
    There are 17 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T0 extends java.lang.Comparable,T1 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: T1[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: double[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: float[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      Note: Java generics information - <T0 extends java.lang.Comparable>
      
      :param seriesName: java.lang.Comparable
      :param categories: T0[]
      :param values: int[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().piePlot(*args)


def plot(*args):
    """
    See Figure.plot(java.lang.Comparable, groovy.lang.Closure<T>)
    
    There are 86 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param function: groovy.lang.Closure<T>
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param function: java.util.function.DoubleUnaryOperator
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: T1[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      Note: Java generics information - <T0 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: double[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().plot(*args)


def plot3d(*args):
    """
    See Figure.plot3d(java.lang.Comparable, groovy.lang.Closure<T>)
    
    There are 733 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param function: groovy.lang.Closure<T>
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param function: java.util.function.DoubleBinaryOperator
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 3*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number,T2 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: T1[]
      :param z: T2[]
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 4*  
      Note: Java generics information - <T0 extends java.lang.Number,T1 extends java.lang.Number>
      
      :param seriesName: java.lang.Comparable
      :param x: T0[]
      :param y: T1[]
      :param z: double[]
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().plot3d(*args)


def plot3dBy(seriesName, t, x, y, z, *byColumns):
    """
    See Figure.plot3dBy(java.lang.Comparable, com.illumon.iris.db.tables.Table, java.lang.String, java.lang.String, java.lang.String, java.lang.String...)
    
    :param seriesName: java.lang.Comparable
    :param t: com.illumon.iris.db.tables.Table
    :param x: java.lang.String
    :param y: java.lang.String
    :param z: java.lang.String
    :param byColumns: java.lang.String...
    :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().plot3dBy(seriesName, t, x, y, z, *byColumns)


def plotBy(*args):
    """
    See Figure.plotBy(java.lang.Comparable, com.illumon.iris.db.plot.filters.SelectableDataSet, java.lang.String, java.lang.String, java.lang.String...)
    
    *Overload 1*  
      :param seriesName: java.lang.Comparable
      :param sds: com.illumon.iris.db.plot.filters.SelectableDataSet
      :param x: java.lang.String
      :param y: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
      
    *Overload 2*  
      :param seriesName: java.lang.Comparable
      :param t: com.illumon.iris.db.tables.Table
      :param x: java.lang.String
      :param y: java.lang.String
      :param byColumns: java.lang.String...
      :return: com.illumon.iris.db.plot.Figure
    """
    
    return FigureWrapper().plotBy(*args)


@_convertArguments
def plotStyleNames():
    """
    See PlotStyle.plotStyleNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.plotStyleNames())


@_convertArguments
def scatterPlotMatrix(*args):
    """
    See ScatterPlotMatrix.scatterPlotMatrix(T[]...)
    
    There are 12 overloads, restricting signature summary to first 4:
    *Overload 1*  
      Note: Java generics information - <T extends java.lang.Number>
      
      :param variables: T[]...
      :return: com.illumon.iris.db.plot.composite.ScatterPlotMatrix
      
    *Overload 2*  
      :param variables: double[]...
      :return: com.illumon.iris.db.plot.composite.ScatterPlotMatrix
      
    *Overload 3*  
      :param variables: float[]...
      :return: com.illumon.iris.db.plot.composite.ScatterPlotMatrix
      
    *Overload 4*  
      :param variables: int[]...
      :return: com.illumon.iris.db.plot.composite.ScatterPlotMatrix
    """
    
    return _plotting_convenience_.scatterPlotMatrix(*args)


@_convertArguments
def themeNames():
    """
    See Themes.themeNames()
    
    :return: java.lang.String[]
    """
    
    return list(_plotting_convenience_.themeNames())
