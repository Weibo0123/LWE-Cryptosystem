from lwe.keygen import keygen
import random
import argparse
import sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description="The LWE Cryptosystem")
    parser.add_argument("-m", required=True, type=int, help="Number of rows in A")
    parser.add_argument("-n", required=True, type=int, help="Number of columns in A")
    parser.add_argument("-q", required=True, type=int, help="Modulus")
    parser.add_argument("-s", "--seed", type=int, help="Random seed, default is 123")
    parser.add_argument("-o", "--output", type=str, help="Output file name")
    return parser.parse_args()

def get_parameters():
    args = parse_args()
    m, n, q = args.m, args.n, args.q
    err = [-2, -1, 0, 1, 2]
    seed = 123 if args.seed is None else args.seed
    if q <= 2:
        sys.exit("Modulus must be greater than 2")
    out = None
    if args.output:
        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        out = open(os.path.join(out_dir, args.output), "w")
    return m, n, q, err, seed, out

def print_stdout(A, b, q):
    print("A=")
    for i, row in enumerate(A):
        if i == 0:
            print("[", row, sep="")
        elif i == len(A) - 1:
            print(" ", row, "]", sep="")
        else:
            print(" ", row, sep="")
    print()
    print(f"b={b}")
    print()
    print(f"q={q}")

def print_file(A, b, q, out):
    print("A=", file=out)
    for i, row in enumerate(A):
        if i == 0:
            print("[", row, sep="", file=out)
        elif i == len(A) - 1:
            print(" ", row, "]", sep="", file=out)
        else:
            print(" ", row, sep="", file=out)
    print("", file=out)
    print(f"b={b}", file=out)
    print(f"\nq={q}", file=out)
    print("", file=out)

    out.close()

def main():
    m, n, q, err, seed, out = get_parameters()
    rng = random.Random(seed)
    A, _, _, b = keygen(m,n, q, err, rng)

    if out:
        print_file(A, b, q, out)
    else:
        print_stdout(A, b, q)


if __name__ == "__main__":
    main()
