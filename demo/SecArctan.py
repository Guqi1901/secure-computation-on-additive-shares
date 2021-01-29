from FixedPoint import FXfamily, FXnum
import numpy as np
from constant import const
from tool import *
from SecMul import SecMul
from SecDiv import SecDiv
from SecCmp import SecCmp

famcfrac = FXfamily(const.cfracbit)

def SecArctan(x1, x2):

    # online
    (uTrue, _, _, _, _, _, _) = secretForTest() # generate u
    u = famcfrac(uTrue)
    (ux1, ux2) = SecMul(u, 0, x1, x2)

    (v1, v2) = SecDiv(x1 - u, x2, 1 + ux1, ux2)

    v = limitFixedRangeByMod(v1 + v2)

    (uv1, uv2) = SecMul(0, v, u, 0)

    sign = SecCmp(uv1, uv2, 1, 0)   # the SecMul and SecCmp can be simplified by SecThreeMul

    res1 = np.arctan(float(u))

    res2 = np.arctan(float(v))

    if (sign > 0):
        res2 = res2 - np.sign(v) * np.pi
    
    return (res1, res2)

if __name__ == '__main__':

    num = 10 ** 6
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0

    for i in range(num):

        #(xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = secretForTest()
        (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn) = normSecretForTest()

        # the following code can avoid the extreme situation that v is out of finite field \mathbb{F},
        # it can be used for other protocols too.
        
        #while(1):
            #(res1, res2) = SecArctan(x1, x2)

            #(res3, res4) = SecArctan(x1, x2)

            #delta = 10 ** -3
            #sig1 = SecCmp(res1, res2, res3 + delta, res4)
            #sig2 = SecCmp(res1 + delta, res2, res3, res4)

            #if(sig1 != sig2):
            #    break
        
        (res1, res2) = SecArctan(x1, x2)
        res = limitFixedRangeByMod(res1 + res2)

        errorRes[i] = abs(np.arctan(xTrue) - res)
        if (errorRes[i] > delta):
            errorCount += 1
            #errorRes[i] = errorRes[i - 1]


    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))