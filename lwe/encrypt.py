"""
encrypt.py
"""

import random
from modarith import mod_q

def encrypt(A: list[list[int]], b: list[int], q: int, mu: int) -> tuple[list[int], int]:
    m = len(A)
    n = len(A[0])

    if mu not in (0, 1):
        raise ValueError("mu must be 0 or 1")
    if m == 0:
        raise ValueError("A must be non-empty")
    if len(b) != m:
        raise ValueError("b must have length m")
    if any(len(row) != n for row in A):
        raise ValueError("All rows of A must have length n")

    r = [random.randint(0, 1) for _ in range(n)]

    u = [0] * n
    for i in range(m):
       if r[i] == 1:
           for j in range(m):
               u[i]  = mod_q((u[i] + A[i][j]), q)

    rb = 0
    for i in range(m):
        if r[i] == 1:
            rb = mod_q((rb + b[i]), q)

    v = mod_q(rb + int(mu) * (q // 2), q)

    return r, v


