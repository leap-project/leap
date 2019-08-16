import inspect


# Transforms a function to an empty string if its value is None,
# else it returns the stringified source code for this function.
#
# fn: The function to be stringifed.
def fn_to_string(fn):
    stringified_fn = "" if fn is None else inspect.getsource(fn)
    return stringified_fn
