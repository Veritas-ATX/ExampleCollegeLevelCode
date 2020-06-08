'''
Created on Jan 20, 2019

@author: austinstiefelmaier
'''

import numpy as np
import matplotlib.pyplot as plt

# Most of code taken from Midterm
def genExp(lam):
    u = np.random.random()
    exp = -1.0 / lam * np.log(u)
    return exp

def genGam(n, lam):
    gamma = 0.0
    for i in range(n):
        gamma += genExp(lam)
    return gamma

def genHyper(lam):
    u = np.random.random()
    if u <= 0.1:
        return genExp(1.0 / lam)
    else:
        return genExp(lam)
    
def f1(t):
    return 0.8 + 0.4 * np.sin(2.0 * np.pi * t)

def f2(t):
    return 0.8 + 0.4 * np.sin(0.1 * np.pi * t)

def genArr(t, func, lam):
    time = t
    u1 = np.random.random()
    time -= 1/lam * np.log(u1)
    u2 = np.random.random()
    while u2 > eval(func) / lam:
        u1 = np.random.random()
        time -= 1/lam * np.log(u1)
        u2 = np.random.random()
    return time

def fifo(dist, func):
    times = np.arange(0.0, 3000.05, 0.2)
    q = []
    n = 0
    tA = genArr(0.0, func, 1.2)
    tD = 1000000.0
    for t in times:
        while (tA <= t or tD <= t):
            if tA <= tD:
                temp = tA
                n += 1
                tA = genArr(temp, func, 1.2)
                if n == 1:
                    tD = temp + eval(dist)
            elif tD < tA:
                temp = tD
                n -= 1
                if n == 0:
                    tD = 1000000.0
                else:
                    tD = temp + eval(dist)
        q.append(n)
    return q

def ps(dist, func):
    times = np.arange(0.0, 3000.05, 0.2)
    q = []
    n = 0
    tA = genArr(0.0, func, 1.2)
    tDALL = 1000000.0
    for t in times:
        while (tA <= t or tDALL <= t):
            if tA <= tDALL:
                temp = tA
                n += 1
                tA = genArr(temp, func, 1.2)
                if n == 1:
                    tDALL = temp + eval(dist)
                else: 
                    tDALL += eval(dist)
            elif tDALL < tA:
                n = 0
                tDALL = 1000000.0
        q.append(n)
    return q

def lifo(dist, func):
    times = np.arange(0.0, 3000.05, 0.2)
    q = []
    n = 0
    tA = genArr(0.0, func, 1.2)
    tD = 1000000.0
    r = []
    for t in times:
        while (tA <= t or tD <= t):
            if tA < tD:
                temp = tA
                if n != 0:
                    tD = temp + eval(dist)
                    if len(r) < n:
                        r.append(tD - temp)
                    else:
                        r[n - 1] = tD - temp
                n += 1
                tA = genArr(temp, func, 1.2)
                tD = temp + eval(dist)
            elif tD <= tA:
                temp = tD
                n -= 1
                if n == 0:
                    tD = 1000000.0
                else:
                    tD = temp + r[n - 1]
        q.append(n)
    return q

numTrials = 100
time = np.arange(0.0, 3000.05, 0.2)

dist1 = 'genExp(1.0)'
dist2 = 'genGam(2, 2.0)'
dist3 = 'genHyper(9.0)'
func1 = 'f1(time)'
func2 = 'f2(time)'

FIFOM1 = []
FIFOM2 = []
FIFOG1 = []
FIFOG2 = []
FIFOH1 = []
FIFOH2 = []

PSM1 = []
PSM2 = []
PSG1 = []
PSG2 = []
PSH1 = []
PSH2 = []

LIFOM1 = []
LIFOM2 = []
LIFOG1 = []
LIFOG2 = []
LIFOH1 = []
LIFOH2 = []
for z in range(numTrials):
    q1 = fifo(dist1, func1)
    q2 = fifo(dist1, func2)
    q3 = fifo(dist2, func1)
    q4 = fifo(dist2, func2)
    q5 = fifo(dist3, func1)
    q6 = fifo(dist3, func2)
    
    q7 = ps(dist1, func1)
    q8 = ps(dist1, func2)
    q9 = ps(dist2, func1)
    q10 = ps(dist2, func2)
    q11 = ps(dist3, func1)
    q12 = ps(dist3, func2)
    
    q13 = lifo(dist1, func1)
    q14 = lifo(dist1, func2)
    q15 = lifo(dist2, func1)
    q16 = lifo(dist2, func2)
    q17 = lifo(dist3, func1)
    q18 = lifo(dist3, func2)
    
    if z == 0:
        FIFOM1 = q1
        FIFOM2 = q2
        FIFOG1 = q3
        FIFOG2 = q4
        FIFOH1 = q5
        FIFOH2 = q6
        
        PSM1 = q7
        PSM2 = q8
        PSG1 = q9
        PSG2 = q10
        PSH1 = q11
        PSH2 = q12
        
        LIFOM1 = q13
        LIFOM2 = q14
        LIFOG1 = q15
        LIFOG2 = q16
        LIFOH1 = q17
        LIFOH2 = q18
    else:
        for i in range(len(FIFOM1)):
            FIFOM1[i] += q1[i]
            FIFOM2[i] += q2[i]
            FIFOG1[i] += q3[i]
            FIFOG2[i] += q4[i]
            FIFOH1[i] += q5[i]
            FIFOH2[i] += q6[i]
            
            PSM1[i] += q7[i]
            PSM2[i] += q8[i]
            PSG1[i] += q9[i]
            PSG2[i] += q10[i]
            PSH1[i] += q11[i]
            PSH2[i] += q12[i]
            
            LIFOM1[i] += q13[i]
            LIFOM2[i] += q14[i]
            LIFOG1[i] += q15[i]
            LIFOG2[i] += q16[i]
            LIFOH1[i] += q17[i]
            LIFOH2[i] += q18[i]
for i in range(len(FIFOM1)):
    FIFOM1[i] /= (numTrials * 1.0)
    FIFOM2[i] /= (numTrials * 1.0)
    FIFOG1[i] /= (numTrials * 1.0)
    FIFOG2[i] /= (numTrials * 1.0)
    FIFOH1[i] /= (numTrials * 1.0)
    FIFOH2[i] /= (numTrials * 1.0)
            
    PSM1[i] /= (numTrials * 1.0)
    PSM2[i] /= (numTrials * 1.0)
    PSG1[i] /= (numTrials * 1.0)
    PSG2[i] /= (numTrials * 1.0)
    PSH1[i] /= (numTrials * 1.0)
    PSH2[i] /= (numTrials * 1.0)
            
    LIFOM1[i] /= (numTrials * 1.0)
    LIFOM2[i] /= (numTrials * 1.0)
    LIFOG1[i] /= (numTrials * 1.0)
    LIFOG2[i] /= (numTrials * 1.0)
    LIFOH1[i] /= (numTrials * 1.0)
    LIFOH2[i] /= (numTrials * 1.0)

# Graph of M, vary service discipline, using Arrival Rate 1
plt.plot(time, FIFOM1, time, PSM1, time, LIFOM1)
plt.title('M fixed, vary service discipline, arrival rate 1')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['FIFO', 'PS', 'LIFO-PR'])
plt.show()

# Graph of M, vary service discipline, using Arrival Rate 2
plt.plot(time, FIFOM2, time, PSM2, time, LIFOM2)
plt.title('M fixed, vary service discipline, arrival rate 2')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['FIFO', 'PS', 'LIFO-PR'])
plt.show()

# Graph of E2, vary service discipline, suing Arrival Rate 1
plt.plot(time, FIFOG1, time, PSG1, time, LIFOG1)
plt.title('E2 fixed, vary service discipline, arrival rate 1')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['FIFO', 'PS', 'LIFO-PR'])
plt.show()

# Graph of E2, vary service discipline, using Arrival Rate 2
plt.plot(time, FIFOG2, time, PSG2, time, LIFOG2)
plt.title('E2 fixed, vary service discipline, arrival rate 2')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['FIFO', 'PS', 'LIFO-PR'])
plt.show()

# Graph of H2, vary service discipline, using Arrival Rate 1
plt.plot(time, FIFOH1, time, PSH1, time, LIFOH1)
plt.title('H2 fixed, vary service discipline, arrival rate 1')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['FIFO', 'PS', 'LIFO-PR'])
plt.show()

# Graph of H2, vary service discipline, using Arrival Rate 2
plt.plot(time, FIFOH2, time, PSH2, time, LIFOH2)
plt.title('H2 fixed, vary service discipline, arrival rate 2')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['FIFO', 'PS', 'LIFO-PR'])
plt.show()

# Graph of LIFO-PR, varying service time distribution, using Arrival Rate 1
plt.plot(time, LIFOM1, time, LIFOG1, time, LIFOH1)
plt.title('LIFO-PR fixed, vary service time distribution, arrival rate 1')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['M', 'E2', 'H2'])
plt.show()

# Graph of LIFO-PR, varying service time distribution, using Arrival Rate 2
plt.plot(time, LIFOM2, time, LIFOG2, time, LIFOH2)
plt.title('LIFO-PR fixed, vary service time distribution, arrival rate 2')
plt.xlabel('time')
plt.ylabel('E[Q(t)]')
plt.legend(['M', 'E2', 'H2'])
plt.show()
