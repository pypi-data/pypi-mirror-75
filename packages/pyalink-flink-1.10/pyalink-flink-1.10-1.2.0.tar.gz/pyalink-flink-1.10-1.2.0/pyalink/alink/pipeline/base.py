from .lazy.has_lazy_print_transform_info import HasLazyPrintTransformInfo
from ..batch.base import BatchOperator, BatchOperatorWrapper
from ..common.types.bases.params import Params
from ..common.types.bases.with_params import WithParams
from ..py4j_util import get_java_gateway, get_java_class
from ..stream.base import StreamOperatorWrapper


class Transformer(WithParams, HasLazyPrintTransformInfo):
    def get_j_obj(self):
        return self.j_transformer

    def __init__(self, j_transformer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name = kwargs.pop('name', None)
        clsName = kwargs.pop('CLS_NAME', None)
        self.opType = kwargs.pop('OP_TYPE', 'FUNCTION')
        if j_transformer is None:
            self.j_transformer = get_java_gateway().jvm.__getattr__(clsName)()
        else:
            self.j_transformer = j_transformer

    def transform(self, input):
        if isinstance(input, BatchOperator):
            return BatchOperatorWrapper(self.get_j_obj().transform(input.get_j_obj()))
        else:
            return StreamOperatorWrapper(self.get_j_obj().transform(input.get_j_obj()))

    pass


class TransformerWrapper(Transformer):
    def __init__(self, j_transformer):
        super(TransformerWrapper, self).__init__(j_transformer=j_transformer)


class Model(Transformer):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(Model, self).__init__(j_transformer=model, *args, **kwargs)

    def get_j_obj(self):
        return self.model


class PipelineModel(Model):
    def save(self, *args):
        if len(args) == 0:
            return BatchOperatorWrapper(self.get_j_obj().save())
        else:
            self.get_j_obj().save(args[0])

    @staticmethod
    def load(path_or_operator):
        _j_pipeline_model = get_java_class("com.alibaba.alink.pipeline.PipelineModel")
        pipeline_model = _j_pipeline_model()
        if isinstance(path_or_operator, (str,)):
            path = path_or_operator
            pipeline_model = _j_pipeline_model.load(path)
        else:
            operator = path_or_operator
            pipeline_model = _j_pipeline_model.load(operator.get_j_obj())

        LAZY_PRINT_TRANSFORM_DATA_ENABLED = "lazyPrintTransformDataEnabled"
        LAZY_PRINT_TRANSFORM_DATA_TITLE = "lazyPrintTransformDataTitle"
        LAZY_PRINT_TRANSFORM_DATA_NUM = "lazyPrintTransformDataNum"
        LAZY_PRINT_TRANSFORM_STAT_ENABLED = "lazyPrintTransformStatEnabled"
        LAZY_PRINT_TRANSFORM_STAT_TITLE = "lazyPrintTransformStatTitle"

        for j_transformer in pipeline_model.getTransformers():
            params = Params.fromJson(j_transformer.getParams().toJson())
            transformer = TransformerWrapper(j_transformer)

            if params.get(LAZY_PRINT_TRANSFORM_STAT_ENABLED, False):
                transformer.enableLazyPrintTransformStat(params.get(LAZY_PRINT_TRANSFORM_STAT_TITLE))
            if params.get(LAZY_PRINT_TRANSFORM_DATA_ENABLED, False):
                transformer.enableLazyPrintTransformData(
                    params.get(LAZY_PRINT_TRANSFORM_DATA_NUM),
                    params.get(LAZY_PRINT_TRANSFORM_DATA_TITLE))

        return PipelineModel(pipeline_model)


class Estimator(WithParams, HasLazyPrintTransformInfo):
    def get_j_obj(self):
        return self.op

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name = kwargs.pop('name', None)
        clsName = kwargs.pop('CLS_NAME', None)
        self.opType = kwargs.pop('OP_TYPE', 'FUNCTION')
        self.op = get_java_gateway().jvm.__getattr__(clsName)()

    @staticmethod
    def wrap_model(j_model):
        model_name = j_model.getClass().getSimpleName()
        import importlib
        model_cls = getattr(importlib.import_module("pyalink.alink.pipeline"), model_name)
        return model_cls(model=j_model)

    def fit(self, input):
        j_model = self.get_j_obj().fit(input.get_j_obj())
        return self.wrap_model(j_model)

    pass


class BaseTuningModel(Model):
    def __init__(self, model=None, *args, **kwargs):
        super(BaseTuningModel, self).__init__(model=model, *args, **kwargs)

    def getReport(self):
        return self.get_j_obj().getReport().toPrettyJson()


class Pipeline(Estimator):
    def __init__(self, *stages):
        super(Estimator, self).__init__()
        j_pipeline = get_java_gateway().jvm.com.alibaba.alink.pipeline.Pipeline
        j_pipeline_stage_base = get_java_gateway().jvm.com.alibaba.alink.pipeline.PipelineStageBase

        self.stages = list(stages)
        num = len(stages)
        args = get_java_gateway().new_array(j_pipeline_stage_base, num)
        for i, stage in enumerate(stages):
            args[i] = stage.get_j_obj()
        self.op = j_pipeline(args)

    def add(self, *args):
        if len(args) == 1:
            index = self.size()
            stage = args[0]
        else:
            index = args[0]
            stage = args[1]
        self.get_j_obj().add(index, stage.get_j_obj())
        self.stages.insert(index, stage)
        return self

    def remove(self, index):
        self.op.remove(index)
        return self.stages.pop(index)

    def get(self, index):
        return self.stages[index]

    def size(self):
        return len(self.stages)

    def fit(self, input):
        return PipelineModel(self.op.fit(input.get_j_obj()))
        pass

    pass


class PipelineWrapper(Pipeline):
    def __init__(self, j_pipeline):
        super(Estimator, self).__init__()
        self.op = j_pipeline

    pass


class TuningEvaluator(WithParams):
    def get_j_obj(self):
        return self.evaluator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls_name = kwargs.pop('CLS_NAME', None)
        self.evaluator = get_java_class(cls_name)()

    def evaluate(self, input):
        return self.get_j_obj().evaluate(input)

    def isLargerBetter(self):
        return self.get_j_obj().isLargerBetter()
