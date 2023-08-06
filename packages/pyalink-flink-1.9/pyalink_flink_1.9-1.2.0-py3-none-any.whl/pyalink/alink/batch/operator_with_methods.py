from .common import ChiSquareTestBatchOp as _ChiSquareTestBatchOp
from .common import CorrelationBatchOp as _CorrelationBatchOp
from .common import EvalBinaryClassBatchOp as _EvalBinaryClassBatchOp
from .common import EvalClusterBatchOp as _EvalClusterBatchOp
from .common import EvalMultiClassBatchOp as _EvalMultiClassBatchOp
from .common import EvalRegressionBatchOp as _EvalRegressionBatchOp
from .common import SummarizerBatchOp as _SummarizerBatchOp
from .common import VectorChiSquareTestBatchOp as _VectorChiSquareTestBatchOp
from .common import VectorCorrelationBatchOp as _VectorCorrelationBatchOp
from .common import VectorSummarizerBatchOp as _VectorSummarizerBatchOp

from .common import AkSourceBatchOp as _AkSourceBatchOp
from .common import AkSinkBatchOp as _AkSinkBatchOp
from .lazy.lazy_evaluation import pipe_j_lazy_to_py_callbacks

from ..common.types.conversion.java_method_call import auto_convert_java_type
from ..common.types.conversion.type_converters import j_value_to_py_value


class EvaluationMetricsCollector:
    @auto_convert_java_type
    def collectMetrics(self):
        return self.collectMetrics()

    def lazyCollectMetrics(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectMetrics,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintMetrics(self, title: str = None):
        return self.lazyCollectMetrics(
            lambda metrics: print(metrics) if title is None else print(title, metrics, sep="\n"))


class EvalBinaryClassBatchOp(_EvalBinaryClassBatchOp, EvaluationMetricsCollector):
    pass


class EvalClusterBatchOp(_EvalClusterBatchOp, EvaluationMetricsCollector):
    pass


class EvalRegressionBatchOp(_EvalRegressionBatchOp, EvaluationMetricsCollector):
    pass


class EvalMultiClassBatchOp(_EvalMultiClassBatchOp, EvaluationMetricsCollector):
    pass


class ChiSquareTestBatchOp(_ChiSquareTestBatchOp):
    @auto_convert_java_type
    def collectChiSquareTest(self):
        return self.collectChiSquareTest()

    def lazyCollectChiSquareTest(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectChiSquareTest,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintChiSquareTest(self, title: str = None):
        return self.lazyCollectChiSquareTest(
            lambda metrics: print(metrics) if title is None else print(title, metrics, sep="\n"))


class CorrelationBatchOp(_CorrelationBatchOp):
    @auto_convert_java_type
    def collectCorrelationResult(self):
        return self.collectCorrelationResult()

    def lazyCollectCorrelation(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectCorrelation,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintCorrelation(self, title: str = None):
        return self.lazyCollectCorrelation(
            lambda results: print(results) if title is None else print(title, results, sep="\n"))


class SummarizerBatchOp(_SummarizerBatchOp):
    @auto_convert_java_type
    def collectSummary(self):
        return self.collectSummary()

    def lazyCollectSummary(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectSummary,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintSummary(self, title: str = None):
        return self.lazyCollectSummary(
            lambda summary: print(summary) if title is None else print(title, summary, sep="\n"))


class VectorChiSquareTestBatchOp(_VectorChiSquareTestBatchOp):
    @auto_convert_java_type
    def collectChiSquareTest(self):
        return self.collectChiSquareTest()

    def lazyCollectChiSquareTest(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectChiSquareTest,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintChiSquareTest(self, title: str = None):
        return self.lazyCollectChiSquareTest(
            lambda results: print(results) if title is None else print(title, results, sep="\n"))


class VectorCorrelationBatchOp(_VectorCorrelationBatchOp):
    @auto_convert_java_type
    def collectCorrelation(self):
        return self.collectCorrelation()

    def lazyCollectCorrelation(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectCorrelation,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintCorrelation(self, title: str = None):
        return self.lazyCollectCorrelation(
            lambda results: print(results) if title is None else print(title, results, sep="\n"))


class VectorSummarizerBatchOp(_VectorSummarizerBatchOp):
    @auto_convert_java_type
    def collectVectorSummary(self):
        return self.collectVectorSummary()

    def lazyCollectVectorSummary(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectVectorSummary,
            callbacks,
            j_value_to_py_value)
        return self

    def lazyPrintVectorSummary(self, title: str = None):
        return self.lazyCollectVectorSummary(
            lambda summary: print(summary) if title is None else print(title, summary, sep="\n"))


class AkSourceBatchOp(_AkSourceBatchOp):
    def setFilePath(self, val):
        from ..common.types.file_system.file_system import FilePath
        if isinstance(val, FilePath):
            val = val.get_j_obj()
        return super(AkSourceBatchOp, self).setFilePath(val)


class AkSinkBatchOp(_AkSinkBatchOp):
    def setFilePath(self, val):
        from ..common.types.file_system.file_system import FilePath
        if isinstance(val, FilePath):
            val = val.get_j_obj()
        return super(AkSinkBatchOp, self).setFilePath(val)
