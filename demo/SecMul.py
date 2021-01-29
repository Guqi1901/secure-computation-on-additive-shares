from FixedPoint import FXfamily, FXnum
from constant import const
from tool import *
import numpy as np

def SecMul(x1, x2, y1, y2):

    # offline
    a = generateFixedSecret()
    b = generateFixedSecret()
    c = limitFixedRangeByMod(a * b)

    a1 = generateFixedShare()
    b1 = generateFixedShare()
    c1 = generateFixedShare()

    a2 = limitFixedRangeByMod(a - a1)
    b2 = limitFixedRangeByMod(b - b1)
    c2 = limitFixedRangeByMod(c - c1)

    # online
    e1 = limitFixedRangeByMod(x1 - a1)
    f1 = limitFixedRangeByMod(y1 - b1)
    e2 = limitFixedRangeByMod(x2 - a2)
    f2 = limitFixedRangeByMod(y2 - b2)

    e = limitFixedRangeByMod(e1 + e2)
    f = limitFixedRangeByMod(f1 + f2)

    res1 = limitFixedRangeByMod(c1 + b1 * e + a1 * f + e * f)
    res2 = limitFixedRangeByMod(c2 + b2 * e + a2 * f)

    return (res1, res2)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        #(yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = secretForTest()

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()
        (yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = normSecretForTest()

        (res1, res2) = SecMul(x1, x2, y1, y2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(xTrue * yTrue - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))