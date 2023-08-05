#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

#############################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
#############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first define_symbols() call
DBTimeZone = None
DBDateTime = None

SECOND = 1000000000
MINUTE = 60*SECOND
HOUR = 60*MINUTE
DAY = 24*HOUR
WEEK = 7*DAY
YEAR = 52*WEEK


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, DBTimeZone
    if _java_type_ is not None:
        return
    # This will raise an exception if the desired object is not the classpath
    _java_type_ = jpy.get_type("com.illumon.iris.db.tables.utils.DBTimeUtils")
    DBTimeZone = jpy.get_type("com.illumon.iris.db.tables.utils.DBTimeZone")
    DBDateTime = jpy.get_type("com.illumon.iris.db.tables.utils.DBDateTime")


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
def autoEpochToTime(epoch):
    return _java_type_.autoEpochToTime(epoch)


@_passThrough
def cappedTimeOffset(original, period, cap):
    return _java_type_.cappedTimeOffset(original, period, cap)


@_passThrough
def convertDate(s):
    return _java_type_.convertDate(s)


@_passThrough
def convertDateQuiet(*args):
    return _java_type_.convertDateQuiet(*args)


@_passThrough
def convertDateTime(s):
    return _java_type_.convertDateTime(s)


@_passThrough
def convertDateTimeQuiet(s):
    return _java_type_.convertDateTimeQuiet(s)


@_passThrough
def convertExpression(formula):
    return _java_type_.convertExpression(formula)


@_passThrough
def convertJimDateTimeQuiet(s):
    return _java_type_.convertJimDateTimeQuiet(s)


@_passThrough
def convertJimMicrosDateTimeQuiet(s):
    return _java_type_.convertJimMicrosDateTimeQuiet(s)


@_passThrough
def convertJimMicrosDateTimeQuietFast(s, timeZone):
    return _java_type_.convertJimMicrosDateTimeQuietFast(s, timeZone)


@_passThrough
def convertJimMicrosDateTimeQuietFastTz(s):
    return _java_type_.convertJimMicrosDateTimeQuietFastTz(s)


@_passThrough
def convertLocalTimeQuiet(s):
    return _java_type_.convertLocalTimeQuiet(s)


@_passThrough
def convertPeriod(s):
    return _java_type_.convertPeriod(s)


@_passThrough
def convertPeriodQuiet(s):
    return _java_type_.convertPeriodQuiet(s)


@_passThrough
def convertTime(s):
    return _java_type_.convertTime(s)


@_passThrough
def convertTimeQuiet(s):
    return _java_type_.convertTimeQuiet(s)


@_passThrough
def createFormatter(timeZoneName):
    return _java_type_.createFormatter(timeZoneName)


@_passThrough
def currentDate(timeZone):
    return _java_type_.currentDate(timeZone)


@_passThrough
def currentDateNy():
    return _java_type_.currentDateNy()


@_passThrough
def currentTime():
    return _java_type_.currentTime()


@_passThrough
def dateAtMidnight(dateTime, timeZone):
    return _java_type_.dateAtMidnight(dateTime, timeZone)


@_passThrough
def dayDiff(start, end):
    return _java_type_.dayDiff(start, end)


@_passThrough
def dayOfMonth(dateTime, timeZone):
    return _java_type_.dayOfMonth(dateTime, timeZone)


@_passThrough
def dayOfMonthNy(dateTime):
    return _java_type_.dayOfMonthNy(dateTime)


@_passThrough
def dayOfWeek(dateTime, timeZone):
    return _java_type_.dayOfWeek(dateTime, timeZone)


@_passThrough
def dayOfWeekNy(dateTime):
    return _java_type_.dayOfWeekNy(dateTime)


@_passThrough
def dayOfYear(dateTime, timeZone):
    return _java_type_.dayOfYear(dateTime, timeZone)


@_passThrough
def dayOfYearNy(dateTime):
    return _java_type_.dayOfYearNy(dateTime)


@_passThrough
def diff(d1, d2):
    return _java_type_.diff(d1, d2)


@_passThrough
def diffDay(start, end):
    return _java_type_.diffDay(start, end)


@_passThrough
def diffNanos(d1, d2):
    return _java_type_.diffNanos(d1, d2)


@_passThrough
def diffYear(start, end):
    return _java_type_.diffYear(start, end)


@_passThrough
def expressionToNanos(formula):
    return _java_type_.expressionToNanos(formula)


@_passThrough
def format(*args):
    return _java_type_.format(*args)


@_passThrough
def formatDate(dateTime, timeZone):
    return _java_type_.formatDate(dateTime, timeZone)


@_passThrough
def formatDateNy(dateTime):
    return _java_type_.formatDateNy(dateTime)


@_passThrough
def formatNy(dateTime):
    return _java_type_.formatNy(dateTime)


@_passThrough
def getExcelDateTime(*args):
    return _java_type_.getExcelDateTime(*args)


@_passThrough
def getFinestDefinedUnit(timeDef):
    return _java_type_.getFinestDefinedUnit(timeDef)


@_passThrough
def getPartitionFromTimestampMicros(dateTimeFormatter, timestampMicros):
    return _java_type_.getPartitionFromTimestampMicros(dateTimeFormatter, timestampMicros)


@_passThrough
def getPartitionFromTimestampMillis(dateTimeFormatter, timestampMillis):
    return _java_type_.getPartitionFromTimestampMillis(dateTimeFormatter, timestampMillis)


@_passThrough
def getPartitionFromTimestampNanos(dateTimeFormatter, timestampNanos):
    return _java_type_.getPartitionFromTimestampNanos(dateTimeFormatter, timestampNanos)


@_passThrough
def getPartitionFromTimestampSeconds(dateTimeFormatter, timestampSeconds):
    return _java_type_.getPartitionFromTimestampSeconds(dateTimeFormatter, timestampSeconds)


@_passThrough
def getZonedDateTime(*args):
    return _java_type_.getZonedDateTime(*args)


@_passThrough
def hourOfDay(dateTime, timeZone):
    return _java_type_.hourOfDay(dateTime, timeZone)


@_passThrough
def hourOfDayNy(dateTime):
    return _java_type_.hourOfDayNy(dateTime)


@_passThrough
def isAfter(d1, d2):
    return _java_type_.isAfter(d1, d2)


@_passThrough
def isBefore(d1, d2):
    return _java_type_.isBefore(d1, d2)


@_passThrough
def lastBusinessDateNy(*args):
    return _java_type_.lastBusinessDateNy(*args)


@_passThrough
def lowerBin(dateTime, intervalNanos):
    return _java_type_.lowerBin(dateTime, intervalNanos)


@_passThrough
def microsOfMilli(dateTime, timeZone):
    return _java_type_.microsOfMilli(dateTime, timeZone)


@_passThrough
def microsOfMilliNy(dateTime):
    return _java_type_.microsOfMilliNy(dateTime)


@_passThrough
def microsToNanos(micros):
    return _java_type_.microsToNanos(micros)


@_passThrough
def microsToTime(micros):
    return _java_type_.microsToTime(micros)


@_passThrough
def millis(dateTime):
    return _java_type_.millis(dateTime)


@_passThrough
def millisOfDay(dateTime, timeZone):
    return _java_type_.millisOfDay(dateTime, timeZone)


@_passThrough
def millisOfDayNy(dateTime):
    return _java_type_.millisOfDayNy(dateTime)


@_passThrough
def millisOfSecond(dateTime, timeZone):
    return _java_type_.millisOfSecond(dateTime, timeZone)


@_passThrough
def millisOfSecondNy(dateTime):
    return _java_type_.millisOfSecondNy(dateTime)


@_passThrough
def millisToDateAtMidnight(millis, timeZone):
    return _java_type_.millisToDateAtMidnight(millis, timeZone)


@_passThrough
def millisToDateAtMidnightNy(millis):
    return _java_type_.millisToDateAtMidnightNy(millis)


@_passThrough
def millisToNanos(millis):
    return _java_type_.millisToNanos(millis)


@_passThrough
def millisToTime(millis):
    return _java_type_.millisToTime(millis)


@_passThrough
def minus(*args):
    return _java_type_.minus(*args)


@_passThrough
def minuteOfDay(dateTime, timeZone):
    return _java_type_.minuteOfDay(dateTime, timeZone)


@_passThrough
def minuteOfDayNy(dateTime):
    return _java_type_.minuteOfDayNy(dateTime)


@_passThrough
def minuteOfHour(dateTime, timeZone):
    return _java_type_.minuteOfHour(dateTime, timeZone)


@_passThrough
def minuteOfHourNy(dateTime):
    return _java_type_.minuteOfHourNy(dateTime)


@_passThrough
def monthOfYear(dateTime, timeZone):
    return _java_type_.monthOfYear(dateTime, timeZone)


@_passThrough
def monthOfYearNy(dateTime):
    return _java_type_.monthOfYearNy(dateTime)


@_passThrough
def nanos(dateTime):
    return _java_type_.nanos(dateTime)


@_passThrough
def nanosOfDay(dateTime, timeZone):
    return _java_type_.nanosOfDay(dateTime, timeZone)


@_passThrough
def nanosOfDayNy(dateTime):
    return _java_type_.nanosOfDayNy(dateTime)


@_passThrough
def nanosOfSecond(dateTime, timeZone):
    return _java_type_.nanosOfSecond(dateTime, timeZone)


@_passThrough
def nanosOfSecondNy(dateTime):
    return _java_type_.nanosOfSecondNy(dateTime)


@_passThrough
def nanosToMicros(nanos):
    return _java_type_.nanosToMicros(nanos)


@_passThrough
def nanosToMillis(nanos):
    return _java_type_.nanosToMillis(nanos)


@_passThrough
def nanosToTime(nanos):
    return _java_type_.nanosToTime(nanos)


@_passThrough
def overrideLastBusinessDateNyFromCurrentDateNy():
    return _java_type_.overrideLastBusinessDateNyFromCurrentDateNy()


@_passThrough
def plus(*args):
    return _java_type_.plus(*args)


@_passThrough
def secondOfDay(dateTime, timeZone):
    return _java_type_.secondOfDay(dateTime, timeZone)


@_passThrough
def secondOfDayNy(dateTime):
    return _java_type_.secondOfDayNy(dateTime)


@_passThrough
def secondOfMinute(dateTime, timeZone):
    return _java_type_.secondOfMinute(dateTime, timeZone)


@_passThrough
def secondOfMinuteNy(dateTime):
    return _java_type_.secondOfMinuteNy(dateTime)


@_passThrough
def secondsToNanos(seconds):
    return _java_type_.secondsToNanos(seconds)


@_passThrough
def secondsToTime(seconds):
    return _java_type_.secondsToTime(seconds)


@_passThrough
def toDateTime(zonedDateTime):
    return _java_type_.toDateTime(zonedDateTime)


@_passThrough
def upperBin(*args):
    return _java_type_.upperBin(*args)


@_passThrough
def year(dateTime, timeZone):
    return _java_type_.year(dateTime, timeZone)


@_passThrough
def yearDiff(start, end):
    return _java_type_.yearDiff(start, end)


@_passThrough
def yearNy(dateTime):
    return _java_type_.yearNy(dateTime)


@_passThrough
def yearOfCentury(dateTime, timeZone):
    return _java_type_.yearOfCentury(dateTime, timeZone)


@_passThrough
def yearOfCenturyNy(dateTime):
    return _java_type_.yearOfCenturyNy(dateTime)
