"""
linalg.py
"""

from .modarith import mod_q

def dot(u: list[int], v: list[int], q: int) -> int:
    assert len(u) == len(v)
    acc = 0
    for a, b in zip(u, v):
        acc += a * b
    return mod_q(acc, q)

def mat_vec(A: list[list[int]], s: list[int], q: int) -> list[int]:
    out = []
    for row in A:
        out.append(dot(row, s, q))
    return out