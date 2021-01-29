from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMul import SecMul

famefrac = FXfamily(const.cfracbit)

def SecDiv(x1, x2, y1, y2):

    # offline
    sign = [-1, 1]
    c_ = generateExpCoverSecret()
    c_sgn = random.choice(sign)

    c = c_sgn * 2 ** float(c_)
    c = famefrac(c)

    c1 = generateFixedShare()
    c2 = limitFixedRangeByMod(c - c1)

    # online
    (cx1, cx2) = SecMul(x1, x2, c1, c2)
    (cy1, cy2) = SecMul(y1, y2, c1, c2)

    cy = limitFixedRangeByMod(cy1 + cy2)

    cyInv = 1/float(cy)
    cyInv = famefrac(cyInv)

    xDivY1 = shareDecMul(cyInv, cx1)
    xDivY2 = shareDecMul(cyInv, cx2)

    return (xDivY1, xDivY2)

if __name__ == '__main__':
    num = 10 ** 6
    delta = 10 ** -3
    errorRes = np.zeros(num)
    errorCount = 0
    for i in range(num):

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = secretForTest()

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()
        #(yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = normSecretForTest()

        if (abs(limitExpRangeByMod(x1_ + x2_) * x1_sgn * x2_sgn - limitExpRangeByMod(y1_ + y2_) * y1_sgn * y2_sgn) > const.cintbit):
            i = i - 1
            continue

        (res1, res2) = SecDiv(x1, x2, y1, y2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(xTrue / yTrue - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))