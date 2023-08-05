from .utils import SimpleJsonEncoder

class AbstractResultPacker(object):
    
    def pack_result(self, result):
        raise NotImplementedError()

    def pack_error(self, error):
        raise NotImplementedError()


class SimpleJsonResultPacker(AbstractResultPacker):

    def pack_result(self, result):
        return {
            "success": True,
            "result": result,
        }

    def pack_error(self, error):
        return {
            "success": False,
            "error": error,
        }
