#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..lazy.extract_model_info_batch_op import ExtractModelInfoBatchOp
from ..lazy.with_model_info_batch_op import WithModelInfoBatchOp
from ..lazy.with_train_info import WithTrainInfo


class LassoRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LassoRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class LdaModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.clustering.lda.LdaModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LdaPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class LdaTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTopicNum(self, val):
        return self._add_param('topicNum', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setOnlineLearningDecay(self, val):
        return self._add_param('onlineLearningDecay', val)

    def setOnlineLearningOffset(self, val):
        return self._add_param('onlineLearningOffset', val)

    def setOnlineSubSamplingRate(self, val):
        return self._add_param('onlineSubSamplingRate', val)

    def setOptimizeDocConcentration(self, val):
        return self._add_param('optimizeDocConcentration', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)


class LeftOuterJoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.LeftOuterJoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LeftOuterJoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)


class LibSvmSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.LibSvmSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LibSvmSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)


class LibSvmSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.LibSvmSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LibSvmSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearClassifierModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.linear.LinearClassifierModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearClassifierModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class LinearRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class LinearRegressorModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.linear.LinearRegressorModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegressorModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearSvmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class LinearSvmTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class LogisticRegressionPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class LogisticRegressionTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class MaxAbsScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.dataproc.MaxAbsScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MaxAbsScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MaxAbsScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class MaxAbsScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MaxAbsScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinMaxScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.dataproc.MinMaxScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinMaxScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MinMaxScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class MinMaxScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MinMaxScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setMin(self, val):
        return self._add_param('min', val)


class MinusAllBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.MinusAllBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinusAllBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinusBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.MinusBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinusBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MultiStringIndexerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MultiStringIndexerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class MultiStringIndexerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MultiStringIndexerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setStringOrderType(self, val):
        return self._add_param('stringOrderType', val)


class MultilayerPerceptronPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.MultilayerPerceptronPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class MultilayerPerceptronTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.MultilayerPerceptronTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setBlockSize(self, val):
        return self._add_param('blockSize', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitialWeights(self, val):
        return self._add_param('initialWeights', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class MySqlSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.MySqlSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MySqlSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setDbName(self, val):
        return self._add_param('dbName', val)

    def setIp(self, val):
        return self._add_param('ip', val)

    def setOutputTableName(self, val):
        return self._add_param('outputTableName', val)

    def setPassword(self, val):
        return self._add_param('password', val)

    def setPort(self, val):
        return self._add_param('port', val)

    def setUsername(self, val):
        return self._add_param('username', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MySqlSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.MySqlSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MySqlSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setDbName(self, val):
        return self._add_param('dbName', val)

    def setInputTableName(self, val):
        return self._add_param('inputTableName', val)

    def setIp(self, val):
        return self._add_param('ip', val)

    def setPassword(self, val):
        return self._add_param('password', val)

    def setPort(self, val):
        return self._add_param('port', val)

    def setUsername(self, val):
        return self._add_param('username', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)


class NGramBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.NGramBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NGramBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setN(self, val):
        return self._add_param('n', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class NaiveBayesModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.NaiveBayesModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class NaiveBayesPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.NaiveBayesPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class NaiveBayesTextModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.NaiveBayesTextModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class NaiveBayesTextPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.NaiveBayesTextPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class NaiveBayesTextTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.NaiveBayesTextTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setModelType(self, val):
        return self._add_param('modelType', val)

    def setSmoothing(self, val):
        return self._add_param('smoothing', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class NaiveBayesTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.NaiveBayesTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setSmoothing(self, val):
        return self._add_param('smoothing', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class NumericalTypeCastBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.NumericalTypeCastBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NumericalTypeCastBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setTargetType(self, val):
        return self._add_param('targetType', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneHotModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.feature.OneHotModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class OneHotPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.OneHotPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneHotTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.OneHotTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)


class OrderByBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.OrderByBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OrderByBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setFetch(self, val):
        return self._add_param('fetch', val)

    def setLimit(self, val):
        return self._add_param('limit', val)

    def setOffset(self, val):
        return self._add_param('offset', val)

    def setOrder(self, val):
        return self._add_param('order', val)


class PcaModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.PcaTrainBatchOp$PcaModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PcaModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class PcaPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.PcaPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PcaPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class PcaTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.PcaTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PcaTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setK(self, val):
        return self._add_param('k', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCalculationType(self, val):
        return self._add_param('calculationType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class PrefixSpanBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.associationrule.PrefixSpanBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PrefixSpanBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemsCol(self, val):
        return self._add_param('itemsCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setMaxPatternLength(self, val):
        return self._add_param('maxPatternLength', val)

    def setMinConfidence(self, val):
        return self._add_param('minConfidence', val)

    def setMinSupportCount(self, val):
        return self._add_param('minSupportCount', val)

    def setMinSupportPercent(self, val):
        return self._add_param('minSupportPercent', val)


class PrintBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.utils.PrintBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PrintBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class PyBinaryScalarFunctionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.executor.udf.python.PyBinaryScalarFunctionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyBinaryScalarFunctionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setResultType(self, val):
        return self._add_param('resultType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class PyBinaryTableFunctionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.executor.udf.python.PyBinaryTableFunctionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyBinaryTableFunctionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setResultTypes(self, val):
        return self._add_param('resultTypes', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class QuantileDiscretizerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.feature.QuantileDiscretizerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class QuantileDiscretizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.QuantileDiscretizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

