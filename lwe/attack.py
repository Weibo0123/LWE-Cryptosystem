"""
attack.py
"""
from modarith import mod_inv, to_signed
from linalg import mat_vec
import itertools
import random

def l1_error(A: list[list[int]] , b: list[int], s: list[int], q: int):
    As = mat_vec(A, s, q)
    e = [to_signed(bi - ai, q) for bi, ai in zip(b, As)]
    return sum(abs(x) for x in e), e

def solve_square_mod(A: list[list[int]], b: list[int], q: int):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]

    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, n):
            if M[i][c] % q != 0:
                pivot = i
                break
        if pivot is None:
            return None

        M[r], M[pivot] = M[pivot], M[r]

        inv = mod_inv(M[r][c], q)
        for j in range(c, n + 1):
            M[r][j] = (M[r][j] * inv) % q

        for i in range(n):
            if i != r and M[i][c] != 0:
                factor = M[i][c]
                for j in range(c, n + 1):
                    M[i][j] = (M[i][j] - factor * M[r][j]) % q

        r += 1

    return [M[i][-1] % q for i in range(n)]

def solve_lwe(A: list[list[int]], b: list[int], q: int, trials=100, err_set=[-2, -1, 0, 1, 2]):
    m = len(A)
    n = len(A[0])
    best = None


    for _ in range(trials):
        idx = random.sample(range(m), n)
        A_sub = [A[i] for i in idx]
        b_sub = [b[i] for i in idx]

        for e_sub in itertools.product(err_set, repeat=n):
            rhs = [(b_sub[i] - e_sub[i]) % q for i in range(n)]

            s = solve_square_mod(A_sub, rhs, q)
            if s is None:
                continue

            score, e_full = l1_error(A, b, s, q)

            if best is None or score < best[0]:
                best = (score, s, e_full)

                if score == 0:
                    return best

    return best

