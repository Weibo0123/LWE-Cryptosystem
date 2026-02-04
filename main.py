from lwe.keygen import keygen
from lwe.attack import solve_lwe
from lwe.reader import read_instance
import random
import argparse
import sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description="The LWE Cryptosystem")
    subparsers = parser.add_subparsers(dest="command", required=True)

    attack_parser = subparsers.add_parser("attack", help="Brute-force search for secret s and error e")

    keygen_parser = subparsers.add_parser("keygen", help="Generate a public key A and a secret key s")
    keygen_parser.add_argument("-m", required=True, type=int, help="Number of rows in A")
    keygen_parser.add_argument("-n", required=True, type=int, help="Number of columns in A")
    keygen_parser.add_argument("-q", required=True, type=int, help="Modulus")
    keygen_parser.add_argument("-s", "--seed", type=int, help="Random seed, default is 123")
    keygen_parser.add_argument("-o", "--output", type=str, help="Output file name")

    return parser.parse_args()

def get_parameters():
    args = parse_args()
    command = args.command
    if command == "attack":
        return command, None, None, None, None, None, None
    m, n, q = args.m, args.n, args.q
    err = [-2, -1, 0, 1, 2]
    seed = 123 if args.seed is None else args.seed
    if q <= 2:
        sys.exit("Modulus must be greater than 2")
    out = None
    if args.output:
        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, args.output)
    return command, m, n, q, err, seed, out

def print_stdout(A, b, s, e, q):
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

    print("\n\n")
    print("Answer:")
    print(f"e = {e}")
    print(f"s = {s}")
    print()

def print_file(A, b, s, e, q, out):
    with open(f"{out}.txt", "w", encoding="utf-8") as f:
        print("A=", file=f)
        for i, row in enumerate(A):
            if i == 0:
                print("[", row, sep="", file=f)
            elif i == len(A) - 1:
                print(" ", row, "]", sep="", file=f)
            else:
                print(" ", row, sep="", file=f)
        print("", file=f)
        print(f"b={b}", file=f)
        print(f"\nq={q}", file=f)
        print("", file=f)
        print("", file=f)
    with open(f"{out}_answere.txt", "w", encoding="utf-8") as f:
        print("Answer:", file=f)
        print(f"e = {e}", file=f)
        print(f"s = {s}", file=f)
        print("", file=f)

def read_file():
    for i in range(1, 6):
        fname = f"./data/instance{i}.txt"
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

def main():
    command, m, n, q, err, seed, out = get_parameters()

    if command == "attack":
        read_file()
    elif command == "keygen":
        rng = random.Random(seed)
        A, s, e, b = keygen(m,n, q, err, rng)
        if out:
            print_file(A, b, s, e, q, out)
        else:
            print_stdout(A, b, s, e, q)


if __name__ == "__main__":
    main()
