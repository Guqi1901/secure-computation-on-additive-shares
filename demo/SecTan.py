from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecSin import SecSin
from SecCos import SecCos
from SecDiv import SecDiv

def SecTan(x1, x2):

    # online
    (sin1, sin2) = SecSin(x1, x2)
    (cos1, cos2) = SecCos(x1, x2)

    return SecDiv(sin1, sin2, cos1, cos2)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0

    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (res1, res2) = SecTan(x1, x2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(np.tan(xTrue) - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))