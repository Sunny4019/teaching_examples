#! /usr/bin/env python

'''
Created on Jan 18, 2016

@author: welling
'''
import numpy as np
import scipy.optimize as op
import writecurve

pathList = []


def vecFun(parmVec, x):
    """Note that xVec can be a numpy array"""
    assert len(parmVec) == 2, 'This example is simple, just 2 parameters'
    return (x * parmVec[1]) + parmVec[0]


def generate(nSamp):
    xVals = np.random.random(nSamp)
    funVals = vecFun((1.7, 2.3), xVals)
    funVals += np.random.normal(0.0, 0.3, nSamp)
#     for a, v in zip(xVals, funVals):
#         print '%s -> %s' % (a, v)
    return (xVals, funVals)


def chiSqr(parmVec, xVals, sampVals):
    global pathList
    pred = vecFun(parmVec, xVals)
    deltaVals = sampVals - pred
    chiSqrVals = deltaVals * deltaVals
    rslt = np.sum(chiSqrVals)
    print " %s -> result %s" % (parmVec, rslt)
    pathList.append((parmVec[0], parmVec[1], rslt))
    return rslt


def gradChiSqr(parmVec, xVals, sampVals):
    pred = vecFun(parmVec, xVals)
    deltaVals = sampVals - pred
    sumDV = np.sum(deltaVals)
    sumXDV = np.sum(xVals * deltaVals)
    rslt = np.array((-2*sumDV, -2*sumXDV))
    return rslt


def sampleGrid(xVals, sampVals):
    edgeLen = 100
    step = 3.0/float(edgeLen - 1)
    grid = np.zeros([edgeLen, edgeLen])
    for i in xrange(edgeLen):
        for j in xrange(edgeLen):
            grid[i, j] = chiSqr([i * step, j * step], xVals, sampVals)
    return grid


def main():
    #method = 'Nelder-Mead'
    #method = 'Powell'
    method = 'CG'
    np.random.seed(1234)  # To repeatedly get the same values
    xVals, sampVals = generate(3000)
    initialGuess = (1.0, 1.0)
    if method in ['CG']:  # requires gradients
        result = op.minimize(chiSqr, initialGuess, args=(xVals, sampVals), method=method,
                             jac=gradChiSqr)
    else:
        result = op.minimize(chiSqr, initialGuess, args=(xVals, sampVals), method=method)
    print result.x
    writecurve.writeCurve(method, [(x, y) for x, y, z in pathList])  # @UnusedVariable

    # The following bit of code samples and saves a grid of chisquared values
#     grid = sampleGrid(xVals, sampVals)
#     import writebov
#     writebov.writeBOV(grid)


if __name__ == '__main__':
    main()
