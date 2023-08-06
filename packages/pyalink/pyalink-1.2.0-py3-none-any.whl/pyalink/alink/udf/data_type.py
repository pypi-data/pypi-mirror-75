class DataType:
    def __init__(self, name):
        self.name = name


class DataTypes(object):
    """
    This DataTypes is a phony one to pyflink.table.types.DataTypes.
    All static methods directly return a string which equals to the return value of calling _to_flink_type_string
    using the same static method in pyflink.
    """

    @staticmethod
    def NULL():
        return DataType("NULL")

    @staticmethod
    def CHAR(length, nullable=True):
        return DataType("STRING")

    @staticmethod
    def VARCHAR(length, nullable=True):
        return DataType("STRING")

    @staticmethod
    def STRING(nullable=True):
        return DataType("STRING")

    @staticmethod
    def BOOLEAN(nullable=True):
        return DataType("BOOLEAN")

    @staticmethod
    def BINARY(length, nullable=True):
        return DataType("PRIMITIVE_ARRAY<TINYINT>")

    @staticmethod
    def VARBINARY(length, nullable=True):
        return DataType("PRIMITIVE_ARRAY<TINYINT>")

    @staticmethod
    def BYTES(nullable=True):
        return DataType("PRIMITIVE_ARRAY<TINYINT>")

    @staticmethod
    def DECIMAL(precision, scale, nullable=True):
        return DataType("BIGDECIMAL")

    @staticmethod
    def TINYINT(nullable=True):
        return DataType("BYTE")

    @staticmethod
    def SMALLINT(nullable=True):
        return DataType("SHORT")

    @staticmethod
    def INT(nullable=True):
        return DataType("INT")

    @staticmethod
    def BIGINT(nullable=True):
        return DataType("BIGINT")

    @staticmethod
    def FLOAT(nullable=True):
        return DataType("FLOAT")

    @staticmethod
    def DOUBLE(nullable=True):
        return DataType("DOUBLE")

    @staticmethod
    def DATE(nullable=True):
        return DataType("DATE")

    @staticmethod
    def TIME(precision=0, nullable=True):
        return DataType("TIME")

    @staticmethod
    def TIMESTAMP(precision=6, nullable=True):
        return DataType("TIMESTAMP")

    @staticmethod
    def TIMESTAMP_WITH_LOCAL_TIME_ZONE(precision=6, nullable=True):
        return DataType("TIMESTAMP")

    @staticmethod
    def ARRAY(element_type, nullable=True):
        return DataType("OBJECT_ARRAY<?>")

    @staticmethod
    def MAP(key_type, value_type, nullable=True):
        return DataType("MAP<?, ?>")

    @staticmethod
    def MULTISET(element_type, nullable=True):
        return DataType("MULTISET<?")

    @staticmethod
    def ROW(row_fields=[], nullable=True):
        return DataType("ROW<?>")

    @staticmethod
    def FIELD(name, data_type, description=None):
        return DataType("FIELD")

    @staticmethod
    def SECOND(precision=None):
        return DataType("SECOND")

    @staticmethod
    def MINUTE():
        return DataType("MINUTE")

    @staticmethod
    def HOUR():
        return DataType("HOUR")

    @staticmethod
    def DAY(precision=None):
        return DataType("DAY")

    @staticmethod
    def MONTH():
        return DataType("MONTH")

    @staticmethod
    def YEAR(precision=None):
        return DataType("YEAR")

    @staticmethod
    def INTERVAL(upper_resolution, lower_resolution=None):
        return DataType("INTERVAL")
