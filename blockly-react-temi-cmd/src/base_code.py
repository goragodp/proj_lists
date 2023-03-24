import math


in_x1 = 0
in_x2 = 0
w1 = 0
w2 = 0
out = (w1 * in_x1) + (w2 * in_x2)
zeta  = 0
alpha = 0.5
y = (1 / (1 + math.exp(-1 * (out - zeta) * alpha)))
print('Output is : {}'.format(y))