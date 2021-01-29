from FixedPoint import FXfamily, FXnum
from constant import const
from tool import *
import numpy as np

def SecMatMul(X1, X2, Y1, Y2):

    # offline
    A = generateFixedSecretMat()
    B = generateFixedSecretMat()
    C = np.dot(A, B)

    A1 = generateFixedShareMat()
    B1 = generateFixedShareMat()
    C1 = generateFixedShareMat()

    A2 = limitFixedMatRangeByMod(A - A1)
    B2 = limitFixedMatRangeByMod(B - B1)
    C2 = limitFixedMatRangeByMod(C - C1)

    # online
    E1 = limitFixedMatRangeByMod(X1 - A1)
    F1 = limitFixedMatRangeByMod(Y1 - B1)
    E2 = limitFixedMatRangeByMod(X2 - A2)
    F2 = limitFixedMatRangeByMod(Y2 - B2)

    E = limitFixedMatRangeByMod(E1 + E2)
    F = limitFixedMatRangeByMod(F1 + F2)

    Res1 = limitFixedMatRangeByMod(C1 + np.dot(E, B1) + np.dot(A1, F) + np.dot(E, F))
    Res2 = limitFixedMatRangeByMod(C2 + np.dot(E, B2) + np.dot(A2, F))

    return (Res1, Res2)

if __name__ == '__main__':

    num = 10 ** 5
    errorRes = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0
    for i in range(num):

        (XTrue, X1, X2) = normSecretMatForTest()
        (YTrue, Y1, Y2) = normSecretMatForTest()

        (Res1, Res2) = SecMatMul(X1, X2, Y1, Y2)
        Res = limitFixedMatRangeByMod(Res1 + Res2)

        Diff = abs(limitFixedMatRangeByMod(np.dot(XTrue, YTrue) - Res))
        errorRes[i] = Diff.flat[Diff.argmax()]
        if (errorRes[i] > delta):
            errorCount += 1

    print(errorCount)
    print(np.mean(errorRes))
    print(np.max(errorRes))