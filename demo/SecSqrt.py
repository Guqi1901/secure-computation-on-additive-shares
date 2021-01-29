from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMulRes import SecMulResForSqrt
from SecMulRes import SecMulRes
from SecAddRes import SecAddRes

famefrac = FXfamily(const.efracbit)

def SecSqrt(x1, x2):

    # online
    (x1_, x2_, x1_sgn, x2_sgn) = SecAddRes(x1, x2)

    res1_ = famefrac(x1_ * 1/2)

    if(res1_ > const.cshareintbit / 2):
        res1_ = res1_ - const.cshareintbit
    elif(res1_ <= - const.cshareintbit / 2):
        res1_ = res1_ + const.cshareintbit

    res2_ = famefrac(x2_ * 1/2)

    if (res2_ > const.cshareintbit / 2):
       res2_ = res2_ - const.cshareintbit
    elif (res2_ <= - const.cshareintbit / 2):
       res2_ = res2_ + const.cshareintbit

    (res1, res2) = SecMulResForSqrt(res1_, res2_)

    return (res1, res2)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errCount = 0
    for i in range(num):

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (res1, res2) = SecSqrt(x1, x2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(np.sqrt(abs(xTrue)) - res)
        if (errorRes[i] > delta):
            errCount += 1

    print(errCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))