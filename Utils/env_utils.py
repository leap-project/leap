# Loads a function named fn_name to context 
# from req if it exists, else from module
def load_fn(fn_name, req, module, context):
    if req[fn_name] == "":
        # If function is not defined
        context[fn_name] = getattr(module, fn_name)
    else:
        exec(req[fn_name], context)

# Loads a function from a function generator that returns a list of functions
def load_from_fn_generator(gen_fn_name, fn_name, req, module, context):
    if req[gen_fn_name] == "":
        gen_fn = getattr(module, gen_fn_name)
        context[fn_name] = gen_fn()
    else:
        exec(req[gen_fn_name], globals())
        gen_fn = getattr(globals(), gen_fn_name)
        context[fn_name] = gen_fn

