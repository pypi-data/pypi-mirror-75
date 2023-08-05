from numpy import asarray, int32, int64, float32, float64

# We may want to use columnar Fortran 'F' order
default_order = 'A'


def int32_(a, order=default_order):
    return asarray(a, dtype=int32, order=order)


def int64_(a, order=default_order):
    return asarray(a, dtype=int64, order=order)


def float32_(a, order=default_order):
    return asarray(a, dtype=float32, order=order)


def float64_(a, order=default_order):
    return asarray(a, dtype=float64, order=order)
