from sage.all import *

pr = PolynomialRing(ZZ, ('c', 'd', 'X1', 'X2', 'Y1', 'Y2'), 6)
c, d, X1, X2, Y1, Y2 = pr.gens()
Z1, Z2 = 1, 1
formula = {}
A = Z1 * Z2
formula['A'] = A
t0 = A ** 2
formula['t0'] = t0
B = d * t0
formula['B'] = B
C = X1 * X2
formula['C'] = C
D = Y1 * Y2
formula['D'] = D
E = C * D
formula['E'] = E
H = C - D
formula['H'] = H
t1 = X1 + Y1
formula['t1'] = t1
t2 = X2 + Y2
formula['t2'] = t2
t3 = t1 * t2
formula['t3'] = t3
t4 = t3 - C
formula['t4'] = t4
I = t4 - D
formula['I'] = I
t5 = E + B
formula['t5'] = t5
t6 = t5 * H
formula['t6'] = t6
X3 = c * t6
formula['X3'] = X3
t7 = E - B
formula['t7'] = t7
t8 = t7 * I
formula['t8'] = t8
Y3 = c * t8
formula['Y3'] = Y3
t9 = H * I
formula['t9'] = t9
Z3 = A * t9
formula['Z3'] = Z3
for key, value in formula.items():
    print(f'{key} = {value}')
