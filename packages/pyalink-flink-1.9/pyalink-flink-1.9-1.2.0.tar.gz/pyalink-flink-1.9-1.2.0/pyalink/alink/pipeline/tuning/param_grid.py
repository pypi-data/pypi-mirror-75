from ...common.types.bases.j_obj_wrapper import JavaObjectWrapper
from ...common.types.conversion.java_method_call import call_java_method
from ...py4j_util import get_java_class


class ParamGrid(JavaObjectWrapper):
    def get_j_obj(self):
        return self.j_param_dist

    def __init__(self):
        self.j_param_dist = get_java_class("com.alibaba.alink.pipeline.tuning.ParamGrid")()
        self.items = []
        pass

    def addGrid(self, stage, info, *args):
        if len(args) <= 0:
            raise Exception("at least 1 item should be provided in addGrid")
        if isinstance(args[0], (list, tuple,)):
            args = args[0]
        call_java_method(self.get_j_obj().addGrid, stage, info, args)
        self.items.append((stage, info, args))
        return self

    def getItems(self):
        return self.items
