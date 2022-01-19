import time
from functools import wraps
from robot.api import logger
from robot.libraries.BuiltIn import register_run_keyword, BuiltIn
from variables.VariablesDictionary import VariablesDictionary

def enable_robot_logging(func):

    @wraps(func)
    def func_wrapper(cls, *args, **kwargs):

        if not hasattr(func, "second"):
            setattr(func, "second", True)
            args = list(args)

            kwargs_list = ["%s=%s" % (key, val) for key, val in kwargs.items()]
            if kwargs_list:
                args.extend(kwargs_list)

            register_run_keyword("WiseLibrary", func.__name__, len(args), deprecation_warning=False)
            return BuiltIn().run_keyword(func.__name__, *args)

        else:
            delattr(func, "second")
            return func(cls, *args, **kwargs)

    return func_wrapper


def time_it(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):

        args = list(args)
        kwargs_list = ["%s=%s" % (key, val) for key, val in kwargs.items()]

        # if kwargs_list:
        #    args.extend(kwargs_list)

        start = time.time()
        ret_value = func(*args, **kwargs)
        end = time.time()
        time_taken = round((end - start), 2)

        global_variables = VariablesDictionary()
        global_variables.update_global_variable("PAGE_LOAD_TIME", {func.__name__: time_taken})
        logger.info("PAGE_LOAD_TIME | %s: %s" % (func.__name__, time_taken))
        return  ret_value

    return func_wrapper

