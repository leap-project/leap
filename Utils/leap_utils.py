import inspect

def fn_to_string(fn):
    stringified_fn = "" if fn is None else inspect.getsource(fn)
    return stringified_fn