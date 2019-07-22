import textwrap
import inspect

def fn_to_str(fn):
    return textwrap.dedent(inspect.getsource(fn))