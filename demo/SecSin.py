from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMulRes import SecMulRes

famefrac = FXfamily(const.efracbit)

def SecSin(x1, x2):

    # online
    t1 = x1.sin()
    t2 = x1.cos()
    t3 = x2.sin()
    t4 = x2.cos()

    (sin11, sin21) = SecMulRes(famefrac(np.log2(float(abs(t1)))), famefrac(np.log2(float(abs(t4)))), np.sign(t1), np.sign(t4))
    (sin12, sin22) = SecMulRes(famefrac(np.log2(float(abs(t3)))), famefrac(np.log2(float(abs(t2)))), np.sign(t3), np.sign(t2))

    sin1 = limitFixedRangeByMod(sin11 + sin12)
    sin2 = limitFixedRangeByMod(sin21 + sin22)

    return (sin1, sin2)

if __name__ == '__main__':

    num = 10 ** 6
    delta = 10 ** -3
    errorRes = np.zeros(num)
    errorCount = 0

    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (res1, res2) = SecSin(x1, x2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(np.sin(xTrue) - res)
        if (errorRes[i] > delta):
            errorCount += 1
            errorRes[i] = errorRes[i-1]


    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))