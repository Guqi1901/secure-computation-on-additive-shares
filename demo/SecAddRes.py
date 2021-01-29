from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMul import SecMul

famcfrac = FXfamily(const.cfracbit)
famefrac = FXfamily(const.efracbit)


def SecAddRes(x1, x2):
    
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
    
    # online phase
    (xc1, xc2) = SecMul(x1, x2, c1, c2)
    xc = limitFixedRangeByMod(xc1 + xc2)
    
    xc_ = np.log2(abs(float(xc)))

    xc_ = famefrac(xc_)
    
    x1_ = limitExpRangeByMod(xc_ - c1_)
    x2_ = - c2_
    x1_sgn = int(np.sign(xc) * c1_sgn)
    if(xc_ < -const.cshareintbit):
        x1_sgn = 0
    
    x2_sgn = c2_sgn
    
    return (x1_, x2_, x1_sgn, x2_sgn)

if __name__ == '__main__':

    num = 10 ** 6
    delta = 10 ** -3
    errorRes = np.zeros(num)
    errorCount = 0
    for i in range(num):

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (x1_, x2_, x1_sgn, x2_sgn) = SecAddRes(x1, x2)

        res = limitExpRangeByMod(x1_ + x2_)
        res = x1_sgn * x2_sgn * (2 ** res)

        errorRes[i] = abs(xTrue - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))