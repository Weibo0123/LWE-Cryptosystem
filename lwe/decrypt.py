"""
decrypt.py
"""
from modarith import mod_q

def decrypt(u: [list[int]], v: int, s: list[int], q: int) -> int:
    us = 0
    for i in range(u):
        us = mod_q((us + u[i] * s[i]), q)

    t = mod_q(v - us, q)

    if q // 4 < t < 3 * q // 4:
        return 1
    return 0