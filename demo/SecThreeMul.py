from FixedPoint import FXfamily, FXnum
import random
from constant import const
from tool import *
import numpy as np

from SecMul import SecMul

def SecThreeMul(x1, x2, y1, y2, z1, z2):

    # offline phase
    a = generateFixedSecret()
    b = generateFixedSecret()
    c = generateFixedSecret()
    abc = limitFixedRangeByMod(a * b * c)

    a1 = generateFixedShare()
    b1 = generateFixedShare()
    c1 = generateFixedShare()
    abc1 = generateFixedShare()

    a2 = limitFixedRangeByMod(a - a1)
    b2 = limitFixedRangeByMod(b - b1)
    c2 = limitFixedRangeByMod(c - c1)
    abc2 = limitFixedRangeByMod(abc - abc1)

    # onine phase
    e1 = limitFixedRangeByMod(x1 - a1)
    f1 = limitFixedRangeByMod(y1 - b1)
    g1 = limitFixedRangeByMod(z1 - c1)

    e2 = limitFixedRangeByMod(x2 - a2)
    f2 = limitFixedRangeByMod(y2 - b2)
    g2 = limitFixedRangeByMod(z2 - c2)

    e = limitFixedRangeByMod(e1 + e2)
    f = limitFixedRangeByMod(f1 + f2)
    g = limitFixedRangeByMod(g1 + g2)

    (yz1, yz2) = SecMul(y1, y2, z1, z2)
    (xz1, xz2) = SecMul(x1, x2, z1, z2)
    (xy1, xy2) = SecMul(x1, x2, y1, y2)

    res1 = limitFixedRangeByMod(abc1 - z1*e*f - y1*e*g - x1*f*g + e*yz1 + f*xz1 + g*xy1 + e*f*g)
    res2 = limitFixedRangeByMod(abc2 - z2*e*f - y2*e*g - x2*f*g + e*yz2 + f*xz2 + g*xy2)

    return (res1, res2)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    errorCount = 0
    delta = 10 ** -3
    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        #(yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = secretForTest()
        #(zTrue, z1, z2, z1_, z2_, z1_sgn, z2_sgn) = secretForTest()

        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()
        (yTrue, y1, y2, y1_, y2_, y1_sgn, y2_sgn) = normSecretForTest()
        (zTrue, z1, z2, z1_, z2_, z1_sgn, z2_sgn) = normSecretForTest()

        (res1, res2) = SecThreeMul(x1, x2, y1, y2, z1, z2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(xTrue * yTrue * zTrue - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))