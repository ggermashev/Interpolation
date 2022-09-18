import math

import matplotlib.pyplot as plt
import numpy as np

def func(x):
    return (np.sin(x-2))**5 + (np.cos(x/10))**7

def equal_step(left,right,step):
    return np.arange(left,right,step)

def chebishev_step(left,right,step):
    count = math.floor((right - left) / step)
    return [(left + right) / 2 + (right - left) / 2 * np.cos(np.pi * (2*i - 1) / (2 * count)) for i in range(1,count+1)]

def new_x(arr):
    res = []
    for i in range(len(arr) - 1):
        res.append((arr[i] + arr[i+1])/2)
    return res

def interp(mainFuncValues, mainFuncNodes, pointX):
    l = 0
    for i in range(len(mainFuncNodes)):
        product = 1
        for k in range(len(mainFuncNodes)):
            if (mainFuncNodes[i] - mainFuncNodes[k] == 0): continue
            product *= (pointX - mainFuncNodes[k]) / (mainFuncNodes[i] - mainFuncNodes[k])
        l += mainFuncValues[i] * product
    return l

def get_error(lPoints, lFunc):
    max = 0
    for i,f in enumerate(lFunc):
        dif = abs(f - func(lPoints[i]))
        if dif > max:  max = dif
    return max


left = 0
right = 10

for step in np.arange(0.1, 2.1, 0.1):
    equalArr = equal_step(left,right,step)
    chebArr = chebishev_step(left,right,step)
    mainFuncEqual = [func(x) for x in equalArr]
    mainFuncCheb = [func(x) for x in chebArr]
    pointsEqual = new_x(equalArr)
    pointsCheb = new_x(chebArr)

    lEqual = [interp(mainFuncEqual,equalArr,pointX) for pointX in pointsEqual]
    lCheb = [interp(mainFuncCheb,chebArr,pointX) for pointX in pointsCheb]

    equalError = get_error(pointsEqual, lEqual)
    chebError = get_error(pointsCheb, lCheb)

    print(equalArr)
    print(mainFuncEqual)
    print(pointsEqual)
    print(lEqual)
    print('---------------')
    print(chebArr)
    print(mainFuncCheb)
    print(pointsCheb)
    print(lCheb)

    graphX = np.arange(left,right,step)

    plt.subplot(1,2,1)
    plt.plot(graphX, func(graphX), ':', color='g', label='default')
    plt.plot(pointsEqual, lEqual, '-^', color = 'r', label='interp with equal step')
    plt.grid()
    plt.legend()
    plt.xlim(0,10)
    plt.ylim(-10,10)
    plt.figtext(0.05, 0.95, f"step: {round(step,1)}", color='g')
    plt.figtext(0.2, 0.9, f"error = {round(equalError,5)}")

    plt.subplot(1,2,2)
    plt.plot(graphX, func(graphX), ':', color = 'g', label='default')
    plt.plot(pointsCheb, lCheb, '-^', color='r', label='interp with Chebishev step')
    plt.grid()
    plt.xlim(0,10)
    plt.ylim(-10,10)
    plt.legend()
    plt.figtext(0.65, 0.9, f"error = {round(chebError,5)}")

    plt.savefig(f"graphs/step_{round(step,1)}.png")
    plt.show()

