from math import sqrt

a_n = 1.0
b_n = 1.0/sqrt(2.0)
t_n = 1.0/4.0
p_n = 1.0

for i in range(4):
    a_n1 = (a_n+b_n)/2.0
    b_n1 = sqrt(a_n*b_n)
    t_n1 = t_n - p_n * ((a_n - a_n1) * (a_n - a_n1))
    p_n1 = 2*p_n

    print((a_n1 + b_n1)**2 / (4*t_n1))
    a_n, b_n, t_n, p_n = a_n1, b_n1, t_n1, p_n1
