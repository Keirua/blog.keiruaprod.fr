---
title: The Gauss-Legendre algorithm
author: Keirua
layout: post
lang: en
image: pi-gauss-legendre.py.png
---

I found a pretty strange piece of code in my code directory recently. The file was a few months old. It was short (around 15 loc). Even though it was called `compute.py`, I had no idea what it was meant to compute:

```python
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
```

So this is some math stuff, but what was I thinking about when I wrote that ? It was easy to see that there was no malware in this, so I ran it.

```bash
$ python compute.py
3.1405792505221686
3.141592646213543
3.141592653589794
3.141592653589794
```

The memory came back. A few months ago, I was interested in finding decimals of pi, so… I wrote a program to do so. That's where this piece of code is **awesome**.

It's a very short program. It expected computing pi to be a complicated task, then I found the [Gauss-Legendre algorithm](https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm). It's trivial to implement. As you can see, 15 loc are enough and it could be [golfed](https://en.wikipedia.org/wiki/Code_golf) a bit more.

It's also beautiful that, despite its simplicity, the algorithm has **quadratic convergence** : the number of correct digits doubles with each iteration of the algorithm. That's way better than Monte-Carlo's algorithm I spoke about earlier, where you need 100 times more iterations to get one more digits.

The core idea is that we will compute the **arithmetic–geometric mean of two numbers cleverly chosen and a relationship between all the values will let us approximate pi**. The [Wikipedia page](https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm) has more details on the derivation of this result.

As for us, with specific initial values for a0, b0, t0 and p0:

$$
a_0 = 1 \\
b_0 = \frac{1}{\sqrt{2.0}} \\
t_0 = 0.25 \\
p_0 = 1
$$

we can compute the next values of the sequence:

$$
a_{n+1} = \frac{a_{n} + b_{n}}{2} \\
b_{n+1} = \sqrt{a_{n}b_{n}} \\
t_{n+1} = t_n + p_n(a_n - a_{n+1})^2 \\
p_{n+1} = 2*p_n
$$

and out of these values, with n large enough, we can compute an approximation of pi:

$$
\pi \approx \frac{(a_n + b_n)^2}{4t_{n}}
$$

Due to the quadratic convergence, n = 4 is already enough to have a good enough approximation.