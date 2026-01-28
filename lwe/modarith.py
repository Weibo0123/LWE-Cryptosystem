def mod_q(x: int, q: int) -> int:
    return x % q

def mod_inv(a: int, q: int) -> int:
    return pow(int(a), -1, q)

def to_signed(x: int, q:int) -> int:
    x %= q
    if x > q // 2:
        x -= q
    return x