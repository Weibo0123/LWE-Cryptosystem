"""
sample.py
"""

def sample_uniform_matrix(m: int, n: int, q: int, rng) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(n)] for _ in range(m)]

def sample_uniform_vector(n: int, q: int, rng) -> list[int]:
    return [rng.randrange(q) for _ in range(n)]

def sample_error_vector(m: int, err_set: list[int], rng) -> list[int]:
    return [rng.choice(err_set) for _ in range(m)]  # signed small ints

def sample_mask_vector(m: int, rng) -> list[int]:
    return [rng.randrange(2) for _ in range(m)]  # 0/1