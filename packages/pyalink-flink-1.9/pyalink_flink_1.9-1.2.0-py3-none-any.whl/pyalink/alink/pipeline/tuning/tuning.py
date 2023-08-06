from ..base import Estimator
from ...py4j_util import get_java_class

__all__ = ['GridSearchCV', 'GridSearchTVSplit']


class BaseTuning(Estimator):
    def get_j_obj(self):
        return self.j_tuning

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls_name = kwargs.pop('CLS_NAME', None)
        self.j_tuning = get_java_class(cls_name)()

    def setEstimator(self, estimator):
        self.get_j_obj().setEstimator(estimator.get_j_obj())
        return self

    def setTuningEvaluator(self, tuning_evaluator):
        self.get_j_obj().setTuningEvaluator(tuning_evaluator.get_j_obj())
        return self


class BaseGridSearch(BaseTuning):
    def __init__(self, *args, **kwargs):
        super(BaseGridSearch, self).__init__(*args, **kwargs)

    def setParamGrid(self, value):
        self.get_j_obj().setParamGrid(value.get_j_obj())
        return self


class GridSearchCV(BaseGridSearch):
    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = 'com.alibaba.alink.pipeline.tuning.GridSearchCV'
        kwargs['OP_TYPE'] = 'FUNCTION'
        super(GridSearchCV, self).__init__(*args, **kwargs)

    def setNumFolds(self, value):
        return self._add_param("NumFolds", value)


class GridSearchTVSplit(BaseGridSearch):
    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = 'com.alibaba.alink.pipeline.tuning.GridSearchTVSplit'
        kwargs['OP_TYPE'] = 'FUNCTION'
        super(GridSearchTVSplit, self).__init__(*args, **kwargs)

    def setTrainRatio(self, value):
        return self._add_param("trainRatio", value)
