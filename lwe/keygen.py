"""
keygen.py
"""

from .sample import sample_uniform_matrix, sample_uniform_vector, sample_error_vector
from .linalg import mat_vec
from .modarith import mod_q

def keygen(m: int ,n: int, q: int, err_set: list[int], rng) -> tuple[list[list[int]], list[int], list[int], list[int]]:
    A = sample_uniform_matrix(m, n, q, rng)
    s = sample_uniform_vector(n, q, rng)
    As = mat_vec(A, s, q)
    e = sample_error_vector(m, err_set, rng)
    b = []
    for i in range(m):
        b.append(mod_q(As[i] + e[i], q))
    return A, s, e, b
