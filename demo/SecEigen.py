from FixedPoint import FXfamily, FXnum
import random
from constant import const
from tool import *
import numpy as np

from SecMatMul import SecMatMul
from SecMatInv import SecMatInv
from SecDiv import SecDiv
from SecMul import SecMul

famefrac = FXfamily(const.cfracbit)

def SecEigen(X1, X2):

    # offline
    while(1):
        (t, _, _, _, _, _, _) = secretForTest()
        t = famefrac(abs(t))
        t1 = generateFixedShare()
        t2 = limitFixedRangeByMod(t - t1)

    # online
        (P, P1, P2) = secretMatForTest()
        (PInv1, PInv2) = SecMatInv(P1, P2)

        (tInv1, tInv2) = SecDiv(1, 0, t1, t2)

        (temp1, temp2) = SecMatMul(PInv1, PInv2, X1, X2)
        (temp1, temp2) = SecMatMul(temp1, temp2, P1, P2)

        Y = np.zeros((const.dim, const.dim))
        Y1 = np.zeros((const.dim, const.dim), dtype=FXfamily)
        Y2 = np.zeros((const.dim, const.dim), dtype=FXfamily)

        for i in range(const.dim):
            for j in range(const.dim):
                (Y1[i, j], Y2[i, j]) = SecMul(t1, t2, temp1[i, j], temp2[i, j])

        Y = limitFixedMatRangeByMod(Y1 + Y2).astype(float)

        e_vals, e_vecs = np.linalg.eig(Y)

        if(np.sum(np.isreal(e_vals) -1) == 0):
            break

    sorted_indices = np.argsort(e_vals)
    e_vals = e_vals[sorted_indices[::-1]].astype(FXfamily)
    F = e_vecs[:, sorted_indices[::-1]].astype(FXfamily)

    lambda1 = np.zeros(const.dim, dtype=FXfamily)
    lambda2 = np.zeros(const.dim, dtype=FXfamily)

    for i in range(e_vals.shape[0]):
        lambda1[i] = limitFixedRangeByMod(tInv1 * e_vals[i])
        lambda2[i] = limitFixedRangeByMod(tInv2 * e_vals[i])

    V1 = np.dot(P1, F)
    V2 = np.dot(P2, F)

    return (lambda1, lambda2, V1, V2)

if __name__ == '__main__':
    num = 10 ** 5
    errorRes1 = np.zeros(num)
    errorRes2 = np.zeros(num)
    delta = 10 ** -3
    errorCount = 0

    for j in range(num):

        (XTrue, _, _) = normSecretMatForTest()
        XTrue = np.dot(XTrue.T, XTrue)

        X = XTrue.astype(FXfamily)
        X1 = generateFixedSecretMat()
        X2 = limitFixedMatRangeByMod(X - X1)

        (eigenValue1, eigenValue2, eigenVector1, eigenVector2) = SecEigen(X1, X2)

        eigenValue = np.zeros(const.dim)
        for i in range(const.dim):
            eigenValue[i] = limitFixedRangeByMod(eigenValue1[i] + eigenValue2[i])

        eigenVector = limitFixedMatRangeByMod(eigenVector1 + eigenVector2)

        for i in range(const.dim):
            eigenValue[i] = limitFixedRangeByMod(eigenValue[i])

        (TrueEigenValue, TrueEigenVector) = np.linalg.eig(XTrue)

        sorted_indices = np.argsort(TrueEigenValue)
        TrueValue = TrueEigenValue[sorted_indices[::-1]]
        TrueVector = TrueEigenVector[:, sorted_indices[::-1]]

        Diff1 = abs(TrueValue - eigenValue)

        for i in range(eigenVector.shape[1]):
            a = np.linalg.norm(eigenVector[:, i])
            eigenVector[:, i] = eigenVector[:, i] / a
            
        for i in range(TrueVector.shape[1]):
            a = np.linalg.norm(TrueVector[:, i])
            TrueVector[:, i] = TrueVector[:, i] / a

        for i in range(eigenVector.shape[1]):
            if (np.sign(eigenVector[1, i]) != np.sign(TrueVector[1, i])):
                eigenVector[:, i] = - eigenVector[:, i]

        Diff2 = abs(TrueVector - eigenVector)

        errorRes1[j] = Diff1.flat[Diff1.argmax()]
        errorRes2[j] = Diff2.flat[Diff2.argmax()]

        if (errorRes1[j] > delta or errorRes2[j] > delta):
            errorCount += 1

        print(j)

    print(errorCount)

    print(np.mean(errorRes1))
    print(np.max(errorRes1))

    print(np.mean(errorRes2))
    print(np.max(errorRes2))