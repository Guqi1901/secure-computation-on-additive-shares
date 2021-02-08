from FixedPoint import FXfamily, FXnum
import random
from constant import const
import numpy as np

famcfrac = FXfamily(const.cfracbit)
famefrac = FXfamily(const.efracbit)

# generate the first kind of input
def secretForTest():
    sign = [-1, 1]
    x_ = generateExpSecret()
    x1_ = generateExpShare()
    x2_ = limitExpRangeByMod(x_ - x1_)

    x_sgn = random.choice(sign)
    x1_sgn = random.choice(sign)
    x2_sgn = x_sgn * x1_sgn

    xTrue = x_sgn * 2 ** float(x_)
    x = famcfrac(xTrue)

    x1 = generateFixedShare()
    x2 = limitFixedRangeByMod(x - x1)

    return (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn)

# generate the second kind of input
def normSecretForTest():
    sign = [-1, 1]
    x_ = generateNormExpSecret()
    x1_ = generateExpShare()
    x2_ = limitExpRangeByMod(x_ - x1_)

    x_sgn = random.choice(sign)
    x1_sgn = random.choice(sign)
    x2_sgn = x_sgn * x1_sgn

    xTrue = x_sgn * 2 ** float(x_)
    x = famcfrac(xTrue)

    x1 = generateFixedShare()
    x2 = limitFixedRangeByMod(x - x1)

    return (xTrue, x1, x2, x1_, x2_, x1_sgn, x2_sgn)

# generate the matrix composed by the first kind of input, it is used for covering the true secret
def secretMatForTest():
    sign = [-1, 1]
    xTrue = np.zeros((const.dim, const.dim))
    x1 = np.zeros((const.dim, const.dim), dtype=FXfamily)
    x2 = np.zeros((const.dim, const.dim), dtype=FXfamily)
    for i in range(const.dim):
        for j in range(const.dim):
            x_ = generateExpSecret()
            x_sgn = random.choice(sign)
        
            xTrue[i, j] = x_sgn * 2 ** float(x_)
            x = famcfrac(xTrue[i, j])
        
            x1[i,j] = generateFixedShare()
            x2[i,j] = limitFixedRangeByMod(x - x1[i, j])

    return (xTrue, x1, x2)

# generate the matrix composed by the second kind of input, it is used for testing the precision
def normSecretMatForTest():
    sign = [-1, 1]
    xTrue = np.zeros((const.dim, const.dim))
    x1 = np.zeros((const.dim, const.dim), dtype=FXfamily)
    x2 = np.zeros((const.dim, const.dim), dtype=FXfamily)
    for i in range(const.dim):
        for j in range(const.dim):
            x_ = generateNormExpSecret()
            x_sgn = random.choice(sign)

            xTrue[i, j] = x_sgn * 2 ** float(x_)
            x = famcfrac(xTrue[i, j])

            x1[i, j] = generateFixedShare()
            x2[i, j] = limitFixedRangeByMod(x - x1[i, j])

    return (xTrue, x1, x2)

# multiplication between plaintext and secret (share)
def shareDecMul(x, y):

    res = limitFixedRangeByMod(x * y)

    return res

# ensure the share in a ring \mathbb{Z}_{const.cshareintbit + const.cfracbit}, it could be faster with bit operations
def limitFixedRangeByMod(x):

    N = (2 ** (const.cintbit + 1) - 1) * (2 ** const.cfracbit)

    t = int(x / N)
    x -= t * N

    if(x > N/2 - 1):
        x = x - N
    elif(x < - N/2):
        x = x + N
    
    return x

# ensure all the elements in matrix in the ring
def limitFixedMatRangeByMod(X):
    #for i in range(const.dim):
    #    for j in range(const.dim):
    #        X[i, j] = limitFixedRangeByMod(X[i, j])
    function_vector = np.vectorize(limitFixedRangeByMod)

    X = function_vector(X)

    return X

# it should be used by \mathcal{T}
def generateFixedSecret():
    aInt = random.randint(-(2 ** const.cintbit - 1), 2 ** const.cintbit - 1)
    aFloat = random.random()
    aFloat = famcfrac(aFloat)

    return aInt + aFloat

def generateFixedSecretMat():
    A = np.zeros((const.dim, const.dim), dtype=FXfamily)
    for i in range(const.dim):
        for j in range(const.dim):
            A[i, j] = generateFixedSecret()

    return A

# generate share in the ring
def generateFixedShare():
    a1Int = random.randint(-(2 ** const.cintbit - 1) * (2 ** const.cshareintbit),
                           (2 ** const.cintbit - 1) * (2 ** const.cshareintbit) - 1)
    a1Float = random.random()
    a1Float = famcfrac(a1Float)

    return a1Int + a1Float

# generate share of matrix in the ring
def generateFixedShareMat():
    A = np.zeros((const.dim, const.dim), dtype=FXfamily)
    for i in range(const.dim):
        for j in range(const.dim):
            A[i, j] = generateFixedShare()

    return A

# ensure multiplicative share in the ring [-shareintbit, shareintbit]
def limitExpRangeByMod(x, c = const.cshareintbit):

    while(x > c):
        x = x - 2 * c
    while (x <= -1 * c):
        x = x + 2 * c

    return x

# generate random secret whose exponent in the ring [-intbit, intbit]
def generateExpSecret():
    aInt = random.randint(-const.cintbit, const.cintbit - 1)
    aFloat = random.random()
    aFloat = famcfrac(aFloat)

    return aInt + aFloat

# generate random secret whose exponent under the normal distribution
def generateNormExpSecret():
    return np.random.normal()

# generate secret for covering the true secret, it should be executed by \mathcal{T}
def generateExpCoverSecret():
    aInt = random.randint(-(const.cshareintbit - const.cintbit), const.cshareintbit - const.cintbit - 1)
    aFloat = random.random()
    aFloat = famefrac(aFloat)

    return aInt + aFloat

# change the ring for sqrt computation
def generateExpCoverSecretForSqrt():
    aInt = random.randint(-(const.cshareintbit/2 - const.cintbit/2), const.cshareintbit/2 - const.cintbit/2 - 1)
    aFloat = random.random()
    aFloat = famefrac(aFloat)

    return aInt + aFloat

# generate the share in the ring [-shareintbit, cshareintbit]
def generateExpShare():
    aInt = random.randint(-const.cshareintbit, const.cshareintbit-1)
    aFloat = random.random()
    aFloat = famefrac(aFloat)

    return aInt + aFloat

# change the ring for sqrt
def generateExpShareForSqrt():
    aInt = random.randint(-const.cshareintbit/2, const.cshareintbit/2 - 1)
    aFloat = random.random()
    aFloat = famefrac(aFloat)

    return aInt + aFloat
