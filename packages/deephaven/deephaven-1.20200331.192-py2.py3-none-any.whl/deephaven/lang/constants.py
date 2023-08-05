import numpy as np
import numpy as np

import numba as nb
from enum import Enum

# TODO: a proper configuration method

# set to true to get ast dumps
debugMode = False
# set to true to get timing info dumps
timingMode = False


class VecMode(Enum):
    """The various modes of operation for vectorizer.

    jit -> basic, prototypical version of the vectorizer.
    Manually increases the arity of all arguments by 1,
    optionally takes an output argument at the end of parameters.
    This may produce a less generalized function,
    but is less flexible in terms of slicing up input data.

    vectorize -> uses @vectorize.  Can allow py objects to pass in and out;
    defaults to nopython=True only if possible (and nopython not explicitly set).
    @vectorize can return values, and accept optional output array at the end of parameters.
    This option can perform very efficiently in most cases, and is the default operation.

    guvectorize -> uses @guvectorize.  Void return type; you supply the output array.
    This option is more complex, but gives more control of cardinality, and unlocks cuda mode.
    If you want to, say, pass the length of a list to the function as a scalar value
    (to avoid wasteful .size checks driving the loop), then you'd need to note that in the numpy signature.

    Requires both a numba signature (similar to all others), and a numpy signature (controls arity of arguments)
    @guvectorize(["void(int32[::1], int32, int32[::1])"], "(n)()->(n)")
    def do_stuff(in, len, out):
      for i in range(0, len):
        out[i] = in[i] + whatever()

    cuda -> same as guvec, but runs on graphic card.

    Do not use cuda unless your expression is complex enough to warrant IO to graphics card.
    You must `conda install cudatoolkit=9.0` if you expect cuda mode to work.
    Be sure to benchmark against other options to determine if this is actually better.
    A plain cpu-bound vectorize can likely win on simple expressions.
    https://stackoverflow.com/questions/52046102/numba-and-guvectorize-for-cuda-target-code-running-slower-than-expected
    """
    jit = 0
    vectorize = 1
    guvectorize = 2
    cuda = 3
    default_mode = vectorize


primitive_types = frozenset([
    np.bool_,
    np.byte,
    np.int,
    np.int_,
    np.uint,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.float32,
    np.float64,
    np.float128
])

# While this value is mutable, you should not really set it more than once,
# and do not expect previously-compiled functions to notice any changes.
# Modifactions should likely be done to this source file, rather than at runtime.
global_seed = {
    # This is all you get for default globals, and __builtins__ may even be too much.
    '__builtins__': __builtins__,
    'numpy': np,
    'np': np,
    'numba': nb,
    'nb': nb,
    'jit': nb.jit,
    'vectorize': nb.vectorize,
    'guvectorize': nb.guvectorize,
}


def default_globals():
    return global_seed.copy()
