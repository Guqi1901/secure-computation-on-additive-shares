from FixedPoint import FXfamily, FXnum
import math
import numpy as np
from constant import const
from tool import *

famcfrac = FXfamily(const.cfracbit)

def SecMulRes(x1_, x2_, x1_sgn, x2_sgn):

    sign = [1,-1]

    # offline
    c_ = generateExpCoverSecret()
    c_sgn = random.choice(sign)

    c1_ = generateExpShare()
    c2_ = limitExpRangeByMod(c_ - c1_)

    c1_sgn = random.choice(sign)
    c2_sgn = c1_sgn * c_sgn

    c = c_sgn * 2 ** float(c_)
    c = famcfrac(c)

    c1 = generateFixedShare()
    c2 = limitFixedRangeByMod(c - c1)

    # online
    alpha1_ = limitExpRangeByMod(x1_ - c1_)
    alpha2_ = limitExpRangeByMod(x2_ - c2_)

    alpha1_sgn = x1_sgn * c1_sgn
    alpha2_sgn = x2_sgn * c2_sgn

    alpha_ = limitExpRangeByMod(alpha1_ + alpha2_)
    alpha_sgn = alpha1_sgn * alpha2_sgn

    alpha = alpha_sgn * 2 ** float(alpha_)
    alpha = famcfrac(alpha)

    x1 = limitFixedRangeByMod(alpha * c1)
    x2 = limitFixedRangeByMod(alpha * c2)

    return (x1, x2)

def SecMulResForSqrt(x1_, x2_):
    sign = [1, -1]
    x1_sgn = 1
    x2_sgn = 1
    # offline

    c_ = generateExpCoverSecretForSqrt()
    c_sgn = random.choice(sign)

    c1_ = generateExpShareForSqrt()
    c2_ = limitExpRangeByMod(c_ - c1_, const.cshareintbit/2)

    c1_sgn = random.choice(sign)
    c2_sgn = c1_sgn * c_sgn

    c = c_sgn * 2 ** float(c_)
    c = famcfrac(c)

    c1 = generateFixedShare()
    c2 = limitFixedRangeByMod(c - c1)

    # online
    alpha1_ = limitExpRangeByMod(x1_ - c1_, const.cshareintbit/2)
    alpha2_ = limitExpRangeByMod(x2_ - c2_, const.cshareintbit/2)

    alpha1_sgn = x1_sgn * c1_sgn
    alpha2_sgn = x2_sgn * c2_sgn

    alpha_ = limitExpRangeByMod(alpha1_ + alpha2_, const.cshareintbit/2)
    alpha_sgn = alpha1_sgn * alpha2_sgn

    alpha = alpha_sgn * 2 ** float(alpha_)
    alpha = famcfrac(alpha)

    x1 = limitFixedRangeByMod(alpha * c1)
    x2 = limitFixedRangeByMod(alpha * c2)

    return (x1, x2)

if __name__ == '__main__':

    sign = [1, -1]
    num = 10 ** 6
    delta = 10 ** -3
    errorRes = np.zeros(num)
    errorCount = 0
    for i in range(num):
  
        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (res1, res2) = SecMulRes(x1_, x2_, x1_sgn, x2_sgn)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(xTrue - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))