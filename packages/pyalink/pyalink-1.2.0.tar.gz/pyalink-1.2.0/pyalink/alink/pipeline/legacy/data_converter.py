from ..base import Transformer


class JsonToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.JsonToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToColumns, self).__init__(*args, **kwargs)
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


class CsvToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.CsvToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToColumns, self).__init__(*args, **kwargs)
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


class KvToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.KvToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToColumns, self).__init__(*args, **kwargs)
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


class VectorToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToColumns, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)