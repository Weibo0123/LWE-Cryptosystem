import pytest
from lwe.keygen import keygen
from lwe.modarith import to_signed, mod_q
from lwe.linalg import dot
import random

def test_keygen():
    err = [-2, -1, 0, 1, 2]
    rng = random.Random(123)
    m = 3
    n = 2
    q = 59
    A, s, e, b = keygen(m,n, q, err, rng)
    assert len(A) == m
    assert len(A[0]) == n
    assert len(s) == n
    assert len(e) == m
    assert len(b) == m
    for i in range(m):
        assert to_signed(mod_q(b[i] - dot(A[i], s, q), q ), q) == e[i]
    assert all(0 < x < q for x in b)
