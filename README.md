## Info

This is a supporting document for the paper [STR: Secure Computation on additive shares using the share-transform-reveal strategy](https://arxiv.org/abs/2009.13153).

> STR: Secure computation on additive shares using the share-transform-reveal strategy
>
> By *Zhihua Xia, Qi Gu, Wenhao Zhou, Lizhi Xiong, Jian Weng, Neal N. Xiong*
>
> This paper is accepted by IEEE Transactions on computers now (doi: 10.1109/TC.2021.3073171). Thanks to the editors and reviewers for their time 
>
> If you have any suggestions or problems with the code or this document, please contact me by email: 634337549@qq.com

We provide the demo codes for all the protocols shown in the paper. For convenience and readability, the demo only uses the (2,2)-threshold assumption, and the interaction operations are not simulated. We try to use the same symbols like that in the paper.

**Please download this md file and open it with some better md readers (e.g., typora) to support LATEX.**

## Usage

The codes use the library **[spfpm](https://github.com/rwpenney/spfpm)** to control the decimal length. Thus, please install it before executing the codes. We have written the test code for each protocol, and you can execute them at will.

If you want to use the protocols in a specific task, please note that we here just provide the demo rather than a library. We believe you should do the following to use the codes in a specific task:

1) ensure all the nonlinear steps in the task (for instance, ReLU layer)

2) rewrite these steps based on the demo and ensure the parallelization is used (always based on the matrix)

3) deploy code (combine each step) in multiple terminals and ensure synchronization

Besides, the user should ensure four parameters before the task: 1) $intbit$: all the values appeared in the task (plain-text state) should in the range $(-2^{intbit}, 2^{intbit})$. 2) $shareintbit$: the true $secret$ will be covered in the range $(-2^{shareintbit}, 2^{shareintbit})$. It should be at least two times of $intbit$. 3) $cfracbit$: the precision of $secret$ and $additive$ $share$. 4) $efracbit$: the precision of $multiplicative$ $share$.

## Detail Consumption in theory

We evaluate the number of computations involved in each protocol. The communication consumptions have been described in the paper; thus, we skip it. We show consumption separately according to the protocol. Note that here $add/sub/mul$ are all executed in a ring. 

| Protocols              |                                    |   offline phase    |                                                             |
| ---------------------- | :--------------------------------: | :----------------: | :---------------------------------------------------------: |
|                        |         $add/sub$ on *ASS*         | $add/sub$ on *MSS* |                           others                            |
| $\texttt{SecMul}$      |              $3(n-1)$              |        $0$         |                    1 $mul$ on *secrets*                     |
| $\texttt{SecMulRes}$   |               $n-1$                |       $n-1$        |                     1 $exp$ on *secret*                     |
| $\texttt{SecAddRes}$   |              $4(n-1)$              |       $n-1$        |          1 $mul$ on *secrets*, 1 $exp$ on *secret*          |
| $\texttt{SecExp}$      |               $n-1$                |       $n-1$        |                     1 $exp$ on *secret*                     |
| $\texttt{SecLog}$      |              $4(n-1)$              |       $n-1$        |          1 $mul$ on *secrets*, 1 $exp$ on *secret*          |
| $\texttt{SecPow}$      |              $5(n-1)$              |      $2(n-1)$      |          1 $mul$ on *secrets*, 2 $exp$ on *secret*          |
| $\texttt{SecSin}$      |          $(n-1)2^{(n-1)}$          |   $(n-1)2^{n-1}$   |                $2^{(n-1)}$ $exp$ on *secret*                |
| $\texttt{SecCmp}$      |              $4(n-1)$              |        $0$         |                    1 $mul$ on *secrets*                     |
| $\texttt{SecDiv}$      |              $7(n-1)$              |        $0$         |                    2 $mul$ on *secrets*                     |
| $\texttt{SecMatMul}$   |            $3d^2(n-1)$             |        $0$         |               1 $matmul$ on *secret matrices*               |
| $\texttt{SecMatInv}$   |            $3d^2(n-1)$             |        $0$         |               1 $matmul$ on *secret matrices*               |
| $\texttt{SecMatEigen}$ |          $(12d^2+4)(n-1)$          |        $0$         | 3 $matmul$ on *secret matrices*, $d^2+1$ $mul$ on *secrets* |
| $\texttt{SecThreeMul}$ |             $13(n-1)$              |        $0$         |                    2 $mul$ on *secrets*                     |
| $\texttt{SecArctan}$   | $\frac{23}{2}n^2-\frac{69}{2}n+23$ |        $0$         |                 $5(n-1)$ $mul$ on *secrets*                 |



| Protocols              |                                                     |                                 |    online phase    |                |                                                              |
| ---------------------- | :-------------------------------------------------: | :-----------------------------: | :----------------: | :------------: | :----------------------------------------------------------: |
|                        |                 $add/sub$ on *ASS*                  |         $mul$ on $ASS$          | $add/sub$ on $MSS$ | $mul$ on *MSS* |                            others                            |
| $\texttt{SecMul}$      |                     $2n^2+2n+1$                     |             $2n+1$              |        $0$         |      $0$       |                              -                               |
| $\texttt{SecMulRes}$   |                         $0$                         |               $n$               |       $2n-1$       |      $0$       |                    $n$ $exp$ on *secret*                     |
| $\texttt{SecAddRes}$   |                      $2n^2+3n$                      |             $2n+1$              |        $1$         |      $0$       |                    $1$ $log$ on *secret*                     |
| $\texttt{SecExp}$      |                         $0$                         |               $n$               |       $2n-1$       |      $0$       |                    $n$ $exp$ on *secret*                     |
| $\texttt{SecLog}$      |                      $2n^2+3n$                      |             $2n+1$              |        $1$         |      $0$       |                    $1$ $log$ on *secret*                     |
| $\texttt{SecPow}$      |                      $2n^2+3n$                      |             $3n+1$              |        $2n$        |      $n$       |        $n$ $exp$ on *secret*, $1$ $log$ on *secret*$         |
| $\texttt{SecSin}$      |                     $2^{n-1}-1$                     |           $n2^{n-1}$            |  $(2n-1)2^{n-1}$   |      $0$       | $n2^{n-1}$ $exp$ on *secret*, $n$ $sin$ and $cos$ on additive $share$ |
| $\texttt{SecCmp}$      |                     $3n^2+2n+1$                     |             $2n+1$              |        $0$         |      $0$       |                              -                               |
| $\texttt{SecDiv}$      |                     $5n^2+3n+2$                     |            $5n^2+2$             |        $0$         |      $0$       |                $n$ $div$ on *secret* (with 1)                |
| $\texttt{SecMatMul}$   |                 $2d^2n^2+2d^3n+d^3$                 |           $2d^3n+d^3$           |        $0$         |      $0$       |                              -                               |
| $\texttt{SecMatInv}$   |             $3d^2n^2+(3d^3-2d^2)n+d^3$              |           $3d^3n+d^3$           |        $0$         |      $0$       |               $n$ $matInv$ on *secret matrix*                |
| $\texttt{SecMatEigen}$ |          $(9d^2+3)n^2+$$(8d^3+1)n+3d^3+1$           | $(8d^3+2d^2+d+2)n$+$2d^3+d^2+1$ |        $0$         |      $0$       | $n$ $div$ on *secret* (with 1),  $n$ $matInv$ on *secret matrix*,  $1$ rounds of solving eigenvalue and eigenvector on *secret matrix* |
| $\texttt{SecThreeMul}$ |                    $9n^2+15n+4$                     |             $15n+5$             |        $0$         |      $0$       |                              -                               |
| $\texttt{SecArctan}$   | $\frac{16}{3}n^3+\frac{33}{2}n^2+\frac{115}{6}n-41$ |          $6n^2+14n-20$          |        $0$         |      $0$       | $\frac{1}{2}n^2+\frac{1}{2}n-1$ $div$ on *secrets*, $n$ $arctan$ on *secret* |



## Performance evaluation in practical

### a)

We test the following protocols with two kinds of input *secret*: 1.the exponent is uniformly generated in $[-intbit, intbit]$; 2. the exponent is generated under *the normal distribution*. The sign of *secret* is uniformly random. The $intbit$ of *the secret* is set as 16, the $intbit$ of *share* is set as 48. The $fracbit$ of additive *share* is set as 48/56/64; the $fracbit$ of multiplicative *share* is set as 24/64. The base of multiplicative *share* is . The true *secret* is represented by *float32*.

We test each protocol's actual loss under the different settings; all values result from a million experiments. Compared with the real value, if the experimental error is more than $10^{-3}$, we take it as an error. For example, the loss of *SecMul* is shown in the following table.

*SecMul*: $[xy]_i$ $ \leftarrow $ $[x]_i, [y]_i$ 

|   SecMul    | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :---------: | :------: | :------: | :------: | :------: |
| errorCount1 |    0     |    0     |    0     |    0     |
| meanError1  | 1.29E-09 | 1.30E-09 | 1.32E-09 | 1.30E-09 |
|  maxError1  | 9.45E-07 | 9.52E-07 | 9.52E-07 | 9.45E-07 |
| errorCount2 |    0     |    0     |    0     |    0     |
| meanError2  | 3.52E-15 | 6.55E-17 | 6.47E-17 | 6.46E-17 |
|  maxError2  | 8.52E-14 | 5.44E-15 | 7.01E-15 | 6.59E-15 |

Here, errorCount1 means that under the setting that the exponent is uniformly generated in $[-intbit, intbit]$, the number of errors that is more than *10^3* is 0. The meanError and maxError mean that the actual mean and max loss in all experiments. The following tables are expressed in the same way.

*SecThreeMul*: $[xyz]_i \leftarrow [x]_i, [y]_i, [z]_i$

| SecThreeMul | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :---------: | :------: | :------: | :------: | :------: |
| errorCount1 |   1451   |   1422   |   1462   |   1390   |
| meanError1  | 1.15E-05 | 1.06E-05 | 1.06E-05 | 1.00E-05 |
|  maxError1  |   0.16   |  0.1336  |  0.123   |  0.122   |
| errorCount2 |    0     |    0     |    0     |    0     |
| meanError2  | 1.51E-10 | 5.91E-13 | 2.32E-15 | 2.32E-15 |
|  maxError2  | 1.21E-09 | 4.75E-12 | 2.77E-14 | 3.71E-14 |

*SecMulRes*: $[x]_i \leftarrow <x>_i$

|  SecMulRes  | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
|:-----------:|:--------:|:--------:|:--------:|:--------:|
| errorCount1 |   18110  |    325   |     0    |     0    |
|  meanError1 | 5.19E-04 | 1.97E-06 | 7.59E-09 | 7.61E-09 |
|  maxError1  |   0.88   |   0.003  | 1.15E-05 | 1.43E-05 |
| errorCount2 |     0    |     0    |     0    |     0    |
|  meanError2 | 3.08E-07 | 2.68E-08 | 2.62E-08 | 4.33E-12 |
|  maxError2  | 7.07E-05 | 8.62E-07 | 9.89E-07 | 1.07E-09 |

*SecAddRes*: $<x>_i \leftarrow [x]_i$

|  SecAddRes  | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :---------: | :------: | :------: | :------: | :------: |
| errorCount1 |  83931   |  70595   |  67724   |    0     |
| meanError1  | 8.10E-04 | 3.05E-04 | 2.88E-04 | 7.65E-09 |
|  maxError1  |  0.875   |  0.027   |  0.022   | 1.28E-05 |
| errorCount2 |    0     |    0     |    0     |    0     |
| meanError2  | 2.12E-07 | 6.74E-08 | 6.75E-08 | 2.37E-12 |
|  maxError2  | 7.14E-05 | 2.26E-06 | 2.98E-06 | 1.13E-09 |

*SecExp*: $[a^x]_i \leftarrow [x]_i$, here we choose $a = 2$

|    SecExp   | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
|:-----------:|:--------:|:--------:|:--------:|:--------:|
| errorCount1 |   18026  |    277   |     0    |     0    |
|  meanError1 | 5.09E-04 | 1.92E-06 | 7.46E-09 | 7.49E-09 |
|  maxError1  |   0.89   |   0.003  | 1.20E-05 | 1.10E-05 |
| errorCount2 |     0    |     0    |     0    |     0    |
|  meanError2 | 3.08E-07 | 2.67E-08 | 2.61E-08 | 4.42E-12 |
|  maxError2  | 8.56E-05 | 9.67E-07 | 9.77E-07 | 1.04E-09 |

*SecLog*: $[log_ax]\leftarrow[x]_i$, here we choose $a = 2$

|   SecLog    | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :---------: | :------: | :------: | :------: | :------: |
| errorCount1 |  83976   |  71079   |  68034   |    0     |
| meanError1  | 8.13E-04 | 3.08E-04 | 2.86E-04 | 7.79E-09 |
|  maxError1  |  0.852   |  0.026   |  0.027   | 1.38E-05 |
| errorCount2 |    0     |    0     |    0     |    0     |
| meanError2  | 2.13E-07 | 6.73E-08 | 6.75E-08 | 2.36E-12 |
|  maxError2  | 5.86E-05 | 2.14E-06 | 3.93E-06 | 1.25E-09 |

A special case of *SecPow* ($a=\frac{1}{2}$). Here - means that the error is caused by insufficient $fracbits$ (over the assumption of finite field).

There are two main tricks to this problem:

1) use bigger fractional bit

2) execute two protocols in parallel, after getting the result, use $\texttt{SecCmp}$ to judge that whether the difference of them is less than *delta*

Since the possibility of error is too low (always less than 1/10000), it is necessary to decide whether to use the second trick according to the actual task's risk. The error in the next protocols can all be coped with the above two tricks.

|   SecSqrt   | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :---------: | :------: | :------: | :------: | :------: |
| errorCount1 |    26    |    0     |    0     |    0     |
| meanError1  |    -     | 7.32E-07 | 6.74E-07 | 3.76E-11 |
|  maxError1  |    -     | 2.24E-05 | 2.24E-05 | 2.09E-08 |
| errorCount2 |    0     |    0     |    0     |    0     |
| meanError2  | 9.66E-08 | 2.50E-08 | 2.48E-08 | 1.09E-12 |
|  maxError2  | 1.41E-05 | 2.37E-07 | 2.28E-07 | 2.32E-10 |

*SecSin*: $[sin\theta]_i\leftarrow[\theta]_i$. Here we get rid of extreme error data (always too big) and get more general results

|    SecSin   | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
|:-----------:|:--------:|:--------:|:--------:|:--------:|
| errorCount1 |     1    |     1    |     8    |     2    |
|  meanError1 | 4.03E-07 | 1.81E-08 | 1.81E-08 | 6.05E-12 |
|  maxError1  | 2.78E-05 | 1.17E-07 | 8.12E-08 | 3.77E-10 |
| errorCount2 |     2    |     5    |     1    |     4    |
|  meanError2 | 4.18E-07 | 2.85E-08 | 2.92E-08 | 6.26E-12 |
|  maxError2  | 2.10E-05 | 1.25E-07 | 8.17E-08 | 3.37E-10 |

SecArctan:$[arctan\theta]_i\leftarrow[\theta]_i$

|  SecArctan  | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :---------: | :------: | :------: | :------: | :------: |
| errorCount1 |   7901   |   2838   |    40    |    47    |
| meanError1  |  0.023   |  0.009   | 1.25E-04 | 1.47E-04 |
|  maxError1  |    π     |    π     |    π     |    π     |
| errorCount2 |   123    |    3     |    0     |    0     |
| meanError2  | 9.64E-06 | 1.07E-06 | 7.57E-09 | 7.60E-09 |
|  maxError2  |  3.007   |  0.002   | 2.72E-05 | 1.90E-05 |

### b)

We test the following protocols with only the second kind of input. The protocols on matrices always use the setting of (64, 64); we test three different kinds of matrix size: $4\times4, 16\times16, 64\times64$. Limited by time, the protocols on matrices are only tested $10^5$ times.

*SecDiv*: $\frac{x}{y}_i\leftarrow [x]_i,[y]_i$

|   SecDiv   | (48, 24) | (56, 24) | (64, 24) | (64, 64) |
| :--------: | :------: | :------: | :------: | :------: |
| errorCount |    3     |    0     |    0     |    0     |
| meanError  | 5.76E-07 | 2.24E-09 | 8.64E-12 | 8.63E-12 |
|  maxError  |  0.001   | 1.02E-05 | 2.78E-08 | 3.61E-08 |

*SecMatMul*: $[XY]_i\leftarrow[X]_i, [Y]_i$

| SecMatMul  |   4*4    |  16*16   |  64*64   |
| :--------: | :------: | :------: | :------: |
| errorCount |    0     |    0     |    0     |
| meanError  | 9.27E-16 | 2.84E-15 | 4.79E-14 |
|  maxError  | 3.64E-14 | 5.17E-14 | 1.86E-13 |

*SecMatInv*: $[X^{-1}]_i\leftarrow [X]_i$

| SecMatInv  |   4*4    |  16*16   |  64*64   |
| :--------: | :------: | :------: | :------: |
| errorCount |    0     |    0     |    0     |
| meanError  | 9.07E-12 | 2.74E-11 | 1.07E-10 |
|  maxError  | 2.08E-07 | 1.74E-07 | 2.76E-07 |

*SecMatEigen*: additive $share$ of eigenvalues and eigenvectors of $X $$\leftarrow$ $[X]_i$

|  SecMatEigen  |   4*4    |  16*16   |  64*64   |
| :-----------: | :------: | :------: | :------: |
|  errorCount   |   1301   |    19    |   586    |
| meanValueErr  | 1.61E-03 | 2.98E-06 | 2.28E-05 |
|  maxValueErr  |  2.2695  |  0.001   |  0.005   |
| meanVectorErr | 1.29E-03 | 1.49E-07 | 4.08E-10 |
| maxVectorErr  |  1.898   | 2.32E-04 | 1.19E-07 |

