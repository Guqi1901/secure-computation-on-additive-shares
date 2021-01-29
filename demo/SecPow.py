from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMulRes import SecMulRes
from SecAddRes import SecAddRes

def SecPow(x1, x2, a):

    # online
    (x1_, x2_, x1_sgn, x2_sgn) = SecAddRes(x1, x2)
    x1_ = limitExpRangeByMod(a * x1_)
    x2_ = limitExpRangeByMod(a * x2_)
    (t1, t2) = SecMulRes(x1_, x2_, x1_sgn, x2_sgn)

    return (t1, t2)

if __name__ == '__main__':

    a = 3
    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    famcfrac = FXfamily(const.cfracbit)
    errorCount = 0
    for i in range(num):

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        x = famcfrac(xTrue)
        x1 = generateFixedShare()
        x2 = limitFixedRangeByMod(x - x1)

        (x1, x2) = SecPow(x1, x2, a)
        res = limitFixedRangeByMod(x1 + x2)

        errorRes[i] = abs(xTrue ** a - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))