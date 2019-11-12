import inspect
import string

def retrieve_name_val(var):
        """
        Gets the name of var. Does it from the out most frame inner-wards.
        param var: variable to get name from.
        return: string and value 
        """
        for fi in reversed(inspect.stack()):
            names = [(var_name, var_val) for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]



def raise_type_error(*args):
    for (key, value) in args:
        var_name, var_val = retrieve_name_val(key)
        if not isinstance(var_val, value):
            raise TypeError('the argument {} is not of type "{}"'.format(var_name, value.__name__))