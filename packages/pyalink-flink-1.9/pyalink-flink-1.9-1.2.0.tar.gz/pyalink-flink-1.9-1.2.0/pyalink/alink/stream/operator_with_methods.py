from .common import AkSinkStreamOp as _AkSinkStreamOp
from .common import AkSourceStreamOp as _AkSourceStreamOp


class AkSourceStreamOp(_AkSourceStreamOp):
    def setFilePath(self, val):
        from ..common.types.file_system.file_system import FilePath
        if isinstance(val, FilePath):
            val = val.get_j_obj()
        return super(AkSourceStreamOp, self).setFilePath(val)


class AkSinkStreamOp(_AkSinkStreamOp):
    def setFilePath(self, val):
        from ..common.types.file_system.file_system import FilePath
        if isinstance(val, FilePath):
            val = val.get_j_obj()
        return super(AkSinkStreamOp, self).setFilePath(val)
