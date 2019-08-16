import inspect
import pdb

# Loads a function named fn_name from req into the appropriate
# context. If it doesn't exist, load function from pre-existing
# module.
#
# fn_name: The name of the function we want to load.
# req: The request containing the function to be loaded.
# context: The context where the function will be loaded to.
# module: The module containing the predefined implementation
#         of the function.
def load_fn(fn_name, req, context, module=None):
    if req[fn_name] == "" and module is not None:
        # If function is not defined
        exec(inspect.getsource(getattr(module, fn_name)), context)
    else:
        exec(req[fn_name], context)
        # exec(req[fn_name], context)

# Loads a function from function generator, where the function
# generator is a list of functions.
#
# gen_fn_name: The name of the function generator.
# fn_name: The name of the list of functions we want to load.
# req: The request containing the functions to be loaded.
# context: The context where the functions will be loaded to.
# module: The module where a predefined function may be loaded
#         from.
# gen_fn_args: The arguments that are passed to the funcitons generator.
def load_from_fn_generator(gen_fn_name, fn_name, req, context, module=None, gen_fn_args=None):
    if req[gen_fn_name] == "" and module is not None:
        exec(inspect.getsource(getattr(module, gen_fn_name)), context, globals())
    else:
        exec(req[gen_fn_name], context, globals())
    if gen_fn_args is None:
        context[fn_name] = globals()[gen_fn_name]()
    else:
        context[fn_name] = globals()[gen_fn_name](*tuple(gen_fn_args))

