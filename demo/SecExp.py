from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMulRes import SecMulRes

# for simplicity, we consider that the bases are equal
# notably, the computation itself is in plain; therefore, it is always feasible to adjust the base before executing exp and log

def SecExp(x1, x2):

    # online
    x1 = limitExpRangeByMod(x1)     # if the base is changed, please rewrite limitExpRangeByMod()
    x2 = limitExpRangeByMod(x2)

    (res1, res2) = SecMulRes(x1, x2, 1, 1)

    return (res1, res2)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        (res1, res2) = SecExp(x1_, x2_)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(abs(xTrue) - res)
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))