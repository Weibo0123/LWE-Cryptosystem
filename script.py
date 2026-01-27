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


def solve_square_mod(A, b, q):
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

        inv = modinv(M[r][c], q)
        for j in range(c, n + 1):
            M[r][j] = (M[r][j] * inv) % q

        for i in range(n):
            if i != r and M[i][c] != 0:
                factor = M[i][c]
                for j in range(c, n + 1):
                    M[i][j] = (M[i][j] - factor * M[r][j]) % q

        r += 1

    return [M[i][-1] % q for i in range(n)]


def solve_lwe(A, b, q, trials=100):
    m = len(A)
    n = len(A[0])
    best = None

    ERR = [-2, -1, 0, 1, 2]

    for _ in range(trials):
        idx = random.sample(range(m), n)
        A_sub = [A[i] for i in idx]
        b_sub = [b[i] for i in idx]

        for e_sub in itertools.product(ERR, repeat=n):
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

def parse_matrix(block):
    rows = []
    for line in block.strip().splitlines():
        line = line.strip().replace('[', '').replace(']', '')
        if not line:
            continue
        nums = list(map(int, line.split()))
        rows.append(nums)
    return rows

def parse_vector(text):
    nums = re.findall(r'-?\d+', text)
    return list(map(int, nums))

def read_instance(fname):
    with open(fname) as f:
        txt = f.read()

    A_block = txt.split("A=")[1].split("b=")[0]
    b_block = txt.split("b=")[1].split("q=")[0]
    q = int(txt.split("q=")[1].strip())

    A = parse_matrix(A_block)
    b = parse_vector(b_block)

    return A, b, q

if __name__ == "__main__":
    for i in range(1, 6):
        fname = f"instance{i}.txt"
        print("=" * 60)
        print(fname)

        A, b, q = read_instance(fname)
        res = solve_lwe(A, b, q, trials=120)

        if res is None:
            print("No solution found")
        else:
            score, s, e = res
            print("s =", s)
            print("error =", e)
            print("L1 score =", score)
