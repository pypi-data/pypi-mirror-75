from .lazy_evaluation import pipe_j_lazy_to_py_callbacks
from ..base import BatchOperatorWrapper, BatchOperator
from ...common.types.conversion.java_method_call import auto_convert_java_type
from ...common.types.conversion.type_converters import j_value_to_py_value
from ...common.types.bases.j_obj_wrapper import JavaObjectWrapper


class ExtractModelInfoBatchOp(JavaObjectWrapper):
    def getModelInfoBatchOp(self):
        return BatchOperatorWrapper(self.get_j_obj().getModelInfoBatchOp())

    def lazyPrintModelInfo(self, title=None):
        self.lazyCollectModelInfo(lambda d: print(title, d, sep="\n") if title is not None else print(d))

    @auto_convert_java_type
    def collectModelInfo(self):
        return self.collectModelInfo()

    def lazyCollectModelInfo(self, *callbacks):
        pipe_j_lazy_to_py_callbacks(
            self.get_j_obj().lazyCollectModelInfo,
            callbacks,
            j_value_to_py_value
        )
