#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#
import jpy


__all__ = ['JdbcLogger', 'TableLoggerBase']


TableLoggerBase = None


def defineSymbols():
    """
    Defines appropriate java symbols, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global TableLoggerBase
    if TableLoggerBase is None:
        TableLoggerBase = jpy.get_type("com.illumon.iris.db.tables.dataimport.TableLoggerBase")


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass
