from FixedPoint import FXfamily, FXnum
from constant import const
from tool import *
import numpy as np

from SecMatMul import SecMatMul

def SecMatInv(X1, X2):

    # offline
    (Z, Z1, Z2) = secretMatForTest()

    # online
    (ZX1, ZX2) = SecMatMul(Z1, Z2, X1, X2)

    ZX = limitFixedMatRangeByMod(ZX1 + ZX2)
    ZX = ZX.astype(np.double)
    ZXInv = np.linalg.inv(ZX).astype(FXfamily)

    Res1 = np.dot(ZXInv, Z1)
    Res2 = np.dot(ZXInv, Z2)

    return (Res1, Res2)

if __name__ == '__main__':

    num = 10 ** 5
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        (XTrue, X1, X2) = normSecretMatForTest()

        (Res1, Res2) = SecMatInv(X1, X2)
        Res = limitFixedMatRangeByMod(Res1 + Res2)

        Diff = abs(limitFixedMatRangeByMod(np.linalg.inv(XTrue) - Res))
        errorRes[i] = Diff.flat[Diff.argmax()]
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))