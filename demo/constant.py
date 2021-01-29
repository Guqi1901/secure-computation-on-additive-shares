class Const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)

        self.__dict__[name] = value

const = Const()

const.cintbit = 16          # the range of values in the task (plaintext)
const.cshareintbit = 48     # the range of additive shares
const.cfracbit = 64         # the precision of secret and additive shares
const.efracbit = 64         # the precision of multiplicative shares

const.dim = 16  # the dimension of matrix, it should be determined by the actual task, here we only set it for testing