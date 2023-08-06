from ..base import StreamOperator


class JsonToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.JsonToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class CsvToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.CsvToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setFieldDelimiter(self, val):
        return self._add_param('fieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KvToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.KvToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setColDelimiter(self, val):
        return self._add_param('colDelimiter', val)

    def setValDelimiter(self, val):
        return self._add_param('valDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class VectorToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)