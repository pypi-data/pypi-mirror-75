from .j_obj_wrapper import JavaObjectWrapper


class WithParams(JavaObjectWrapper):

    def __init__(self, *args, **kwargs):
        self.params = dict()

    def _add_param(self, key, val):
        self.params[key] = val
        method_name = "set" + key[:1].upper() + key[1:]
        j_func = self.get_j_obj().__getattr__(method_name)

        from ..conversion.java_method_call import call_java_method
        call_java_method(j_func, val)
        return self
