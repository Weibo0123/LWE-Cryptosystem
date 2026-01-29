from lwe.keygen import keygen
import random
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="The LWE Cryptosystem")
    parser.add_argument("-m", required=True, type=int, help="Number of rows in A")
    parser.add_argument("-n", required=True, type=int, help="Number of columns in A")
    parser.add_argument("-q", required=True, type=int, help="Modulus")
    parser.add_argument("-s", "--seed", type=int, help="Random seed, default is 123")
    parser.add_argument("-o", "--output", type=str, help="Output file name")
    args = parser.parse_args()

    m, n, q = args.m, args.n, args.q
    if q <= 2:
        sys.exit("Modulus must be greater than 2")

    seed = 123 if args.seed is None else args.seed
    if args.output:
        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        out = open(os.path.join(out_dir, args.output), "w")
    err = [-2, -1, 0, 1, 2]
    rng = random.Random(seed)
    A, _, _, b = keygen(m,n, q, err, rng)

    def emit(*args, **kwargs):
        if out:
            print(*args, file=out, **kwargs)
        else:
            print(*args, **kwargs)

    emit("A=")
    for i, row in enumerate(A):
        if i == 0:
            emit("[", row, sep="")
        elif i == len(A) - 1:
            emit(" ", row, "]", sep="")
        else:
            emit(" ", row, sep="")

    emit()
    emit(f"b={b}")
    emit()
    emit(f"q={q}")

    if out:
        out.close()

if __name__ == "__main__":
    main()
