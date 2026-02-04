import itertools
import random
import re

def modinv(a, q):
    return pow(int(a), -1, q)

def to_signed(x, q):
    x %= q
    if x > q // 2:
        x -= q
    return x

def mat_vec(A, s, q):
    out = []
    for row in A:
        v = 0
        for a, b in zip(row, s):
            v = (v + a * b) % q
        out.append(v)
    return out

def l1_error(A, b, s, q):
    As = mat_vec(A, s, q)
    e = [to_signed(bi - ai, q) for bi, ai in zip(b, As)]
    return sum(abs(x) for x in e), e


