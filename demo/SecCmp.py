from FixedPoint import FXfamily, FXnum
import math
import numpy as np
from constant import const
from tool import *
from SecMul import SecMul

famefrac = FXfamily(const.cfracbit)

def SecCmp(x1, x2, y1, y2):

    # offline
    c_ = generateExpCoverSecret()
    c = 2 ** float(c_)
    c = famefrac(c)

    c1 = generateFixedShare()
    c2 = limitFixedRangeByMod(c - c1)

    # online
    diff1 = limitFixedRangeByMod(x1 - y1)
    diff2 = limitFixedRangeByMod(x2 - y2)

    (cx1, cx2) = SecMul(diff1, diff2, c1, c2)

    cx = limitFixedRangeByMod(cx1 + cx2)
    
    if(cx < (2 ** -(const.cfracbit + const.cintbit)) and cx > -(2 ** -(const.cfracbit + const.cintbit))):
        cx = 0
    
    return np.sign(cx)

if __name__ == '__main__':
    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        # (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        # (yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = secretForTest()

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()
        (yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = normSecretForTest()

        res = SecCmp(x1, x2, y1, y2)

        errorRes[i] = abs(np.sign(xTrue - yTrue) - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))