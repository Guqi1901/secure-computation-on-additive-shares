from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecAddRes import SecAddRes

def SecLog(x1, x2):

    # online
    (x1_, x2_, x1_sgn, x2_sgn) = SecAddRes(x1, x2)

    return (x1_, x2_, x1_sgn, x2_sgn)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (x1_, x2_, x1_sgn, x2_sgn) = SecLog(x1, x2)
        res = limitExpRangeByMod(x1_ + x2_)
        res = x1_sgn * x2_sgn * (2 ** res)

        errorRes[i] = abs(xTrue - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))