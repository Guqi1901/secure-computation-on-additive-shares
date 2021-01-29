from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMulRes import SecMulRes

famefrac = FXfamily(const.cfracbit)

def SecCos(x1, x2):

    # online
    t1 = np.sin(x1)
    t2 = np.cos(x1)
    t3 = np.sin(x2)
    t4 = np.cos(x2)

    (cos11, cos21) = SecMulRes(famefrac(np.log2(float(abs(t2)))), famefrac(np.log2(float(abs(t4)))), np.sign(t2), np.sign(t4))
    (cos12, cos22) = SecMulRes(famefrac(np.log2(float(abs(t1)))), famefrac(np.log2(float(abs(t3)))), np.sign(t1), np.sign(t3))

    cos1 = cos11 - cos12
    cos2 = cos21 - cos22

    return (cos1, cos2)

if __name__ == '__main__':
    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (res1, res2) = SecCos(x1, x2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(np.cos(xTrue) - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))