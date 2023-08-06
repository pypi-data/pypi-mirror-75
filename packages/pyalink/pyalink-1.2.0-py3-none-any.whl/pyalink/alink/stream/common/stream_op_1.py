#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import StreamOperator, BaseSinkStreamOp, BaseModelStreamOp


class AftSurvivalRegPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.AftSurvivalRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setQuantileProbabilities(self, val):
        return self._add_param('quantileProbabilities', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class AkSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.AkSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AkSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)


class AkSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.AkSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AkSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class AlsPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.AlsPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class AsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.AsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class BinarizerStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.BinarizerStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinarizerStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setThreshold(self, val):
        return self._add_param('threshold', val)


class BisectingKMeansPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.clustering.BisectingKMeansPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class BucketizerStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.BucketizerStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BucketizerStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCutsArray(self, val):
        return self._add_param('cutsArray', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class ColumnsToCsvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.ColumnsToCsvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToCsvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToJsonStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.ColumnsToJsonStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToJsonStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToKvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.ColumnsToKvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToKvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToTripleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.ColumnsToTripleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToTripleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColValSchemaStr(self, val):
        return self._add_param('tripleColValSchemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToVectorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.ColumnsToVectorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToVectorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)


class CsvSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.CsvSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setFieldDelimiter(self, val):
        return self._add_param('fieldDelimiter', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setRowDelimiter(self, val):
        return self._add_param('rowDelimiter', val)


class CsvSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.CsvSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setFieldDelimiter(self, val):
        return self._add_param('fieldDelimiter', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setLenient(self, val):
        return self._add_param('lenient', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setRowDelimiter(self, val):
        return self._add_param('rowDelimiter', val)

    def setSkipBlankLine(self, val):
        return self._add_param('skipBlankLine', val)


class CsvToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.CsvToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToJsonStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.CsvToJsonStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToJsonStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToKvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.CsvToKvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToKvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToTripleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.CsvToTripleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToTripleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setTripleColValSchemaStr(self, val):
        return self._add_param('tripleColValSchemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToVectorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.CsvToVectorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToVectorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)


class DCTStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.DCTStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DCTStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setInverse(self, val):
        return self._add_param('inverse', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DecisionTreePredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.DecisionTreePredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreePredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DecisionTreeRegPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.DecisionTreeRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DocCountVectorizerPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.DocCountVectorizerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DocHashCountVectorizerPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.DocHashCountVectorizerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class EqualWidthDiscretizerPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.EqualWidthDiscretizerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerPredictStreamOp, self).__init__(*args, **kwargs)
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


class EvalBinaryClassStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.evaluation.EvalBinaryClassStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalBinaryClassStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)


class EvalMultiClassStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.evaluation.EvalMultiClassStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalMultiClassStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)


class FeatureHasherStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.FeatureHasherStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FeatureHasherStreamOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class FilterStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.FilterStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FilterStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class FtrlPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.FtrlPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FtrlPredictStreamOp, self).__init__(*args, **kwargs)
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


class FtrlTrainStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.FtrlTrainStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FtrlTrainStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class GbdtPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.GbdtPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class GbdtRegPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.GbdtRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class GlmPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.GlmPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)


class GmmPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.clustering.GmmPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmPredictStreamOp, self).__init__(*args, **kwargs)
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


class HiveSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.HiveSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HiveSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setDbName(self, val):
        return self._add_param('dbName', val)

    def setHiveConfDir(self, val):
        return self._add_param('hiveConfDir', val)

    def setHiveVersion(self, val):
        return self._add_param('hiveVersion', val)

    def setInputTableName(self, val):
        return self._add_param('inputTableName', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)


class ImputerPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.ImputerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ImputerPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class IndexToStringPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.IndexToStringPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IndexToStringPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setModelName(self, val):
        return self._add_param('modelName', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class IsotonicRegPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.IsotonicRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JdbcRetractSinkStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.JdbcRetractSinkStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JdbcRetractSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JsonToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.JsonToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class JsonToCsvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.JsonToCsvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToCsvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class JsonToKvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.JsonToKvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToKvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class JsonToTripleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.JsonToTripleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToTripleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setTripleColValSchemaStr(self, val):
        return self._add_param('tripleColValSchemaStr', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class JsonToVectorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.JsonToVectorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToVectorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)


class JsonValueStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.JsonValueStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonValueStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonPath(self, val):
        return self._add_param('jsonPath', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSkipFailed(self, val):
        return self._add_param('skipFailed', val)


class KMeansPredictStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.clustering.KMeansPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeansPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class Kafka010SinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.Kafka010SinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Kafka010SinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setBootstrapServers(self, val):
        return self._add_param('bootstrapServers', val)

    def setDataFormat(self, val):
        return self._add_param('dataFormat', val)

    def setTopic(self, val):
        return self._add_param('topic', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setFieldDelimiter(self, val):
        return self._add_param('fieldDelimiter', val)

    def setProperties(self, val):
        return self._add_param('properties', val)


class Kafka010SourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.Kafka010SourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Kafka010SourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setBootstrapServers(self, val):
        return self._add_param('bootstrapServers', val)

    def setGroupId(self, val):
        return self._add_param('groupId', val)

    def setStartupMode(self, val):
        return self._add_param('startupMode', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setProperties(self, val):
        return self._add_param('properties', val)

    def setStartTime(self, val):
        return self._add_param('startTime', val)

    def setTopic(self, val):
        return self._add_param('topic', val)

    def setTopicPattern(self, val):
        return self._add_param('topicPattern', val)

