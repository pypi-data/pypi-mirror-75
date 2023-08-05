
from datacode.models.dtypes.base import DataType


class BooleanType(DataType):
    names = ('bool', 'bool_')

    def __init__(self, categorical: bool = False, ordered: bool = False):
        super().__init__(
            bool,
            categorical=categorical,
            ordered=ordered
        )

    @classmethod
    def from_str(cls, dtype: str, categorical: bool = False, ordered: bool = False):
        dtype = dtype.lower()
        if dtype not in cls.names:
            raise ValueError(f'Dtype {dtype} does not match valid names for {cls.__name__}: {cls.names}')
        return cls(
            categorical=categorical,
            ordered=ordered
        )
