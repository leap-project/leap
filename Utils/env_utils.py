import inspect
import pdb

# Loads a function named fn_name to context 
# from req if it exists, else from module
def load_fn(fn_name, req, context, module=None):
    if req[fn_name] == "" and module is not None:
        # If function is not defined
        exec(inspect.getsource(getattr(module, fn_name)), context)
    else:
        exec(req[fn_name], context)
        # exec(req[fn_name], context)

# Loads a function from a function generator that returns a list of functions
def load_from_fn_generator(gen_fn_name, fn_name, req, context, module=None, gen_fn_args=None):
    if req[gen_fn_name] == "" and module is not None:
        exec(inspect.getsource(getattr(module, gen_fn_name)), context, globals())
    else:
        exec(req[gen_fn_name], context, globals())
    if gen_fn_args is None:
        context[fn_name] = globals()[gen_fn_name]()
    else:
        context[fn_name] = globals()[gen_fn_name](*tuple(gen_fn_args))

