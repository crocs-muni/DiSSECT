from sage.all import *

pr = PolynomialRing(ZZ, ('a', 'b', 'X1', 'X2', 'Y1', 'Y2'), 6)
a, b, X1, X2, Y1, Y2 = pr.gens()
Z1, Z2 = 1, 1
formula = {}
P = X2 - X1
formula['P'] = P
R = Y2 - Y1
formula['R'] = R
PP = P ** 2
formula['PP'] = PP
PPP = P * PP
formula['PPP'] = PPP
Q = X1 * PP
formula['Q'] = Q
t0 = R ** 2
formula['t0'] = t0
t1 = 2 * Q
formula['t1'] = t1
t2 = t0 - PPP
formula['t2'] = t2
X3 = t2 - t1
formula['X3'] = X3
t3 = Q - X3
formula['t3'] = t3
t4 = Y1 * PPP
formula['t4'] = t4
t5 = R * t3
formula['t5'] = t5
Y3 = t5 - t4
formula['Y3'] = Y3
ZZ3 = PP
formula['ZZ3'] = ZZ3
ZZZ3 = PPP
formula['ZZZ3'] = ZZZ3
for key, value in formula.items():
    print(f'{key} = {value}')
