# LWE-Cryptosystem

Learning With Errors (LWE) cryptosystem — a small educational codebase to generate keys, (attempt to) encrypt/decrypt a single bit, and experiment with a simple brute‑force style LWE attack. This repo also includes short math notes to make the notation approachable.

If you are new to the symbols, start with the short notes in [docs/mathematical_conventions.md](docs/mathematical_conventions.md).

## Features
- Key generation: sample public matrix `A`, secret vector `s`, error vector `e`, and compute `b = A s + e (mod q)`
- Brute-force attack demo: try to recover `s` and `e` from `(A, b, q)` by solving many square sub‑instances and scoring the L1 error
- Minimal bit encryption/decryption (work in progress; see caveats)
- Lightweight, no external dependencies

## Mathematical Conventions (very short)
- All arithmetic is modulo `q`.
- Dimensions:
  - `A ∈ Z_q^{m×n}`
  - `s ∈ Z_q^n`
  - `e ∈ small^m`
  - `b = A s + e (mod q)`, so `b ∈ Z_q^m`
- Encryption (intended):
  - `r ∈ {0,1}^m`
  - `u = r^T A ∈ Z_q^n`
  - `v = r^T b + bit * ⎣q/2⎦ (mod q)`

See the docs folder for short primers:
- Modular arithmetic: `docs/math/Modular Arithmetic/*.md`
- Linear algebra: `docs/math/Linear Algebra/*.md`

## Project layout
- `main.py` — CLI entry point (key generation, attack)
- `lwe/keygen.py` — key generation (`A, s, e, b`)
- `lwe/attack.py` — simple randomized sub‑instance solver + L1 error scoring
- `lwe/reader.py` — parse `(A, b, q)` from a text file
- `lwe/encrypt.py`, `lwe/decrypt.py` — minimal bit encryption/decryption (WIP)
- `lwe/modarith.py` — modular helpers (e.g., `mod_q`, `mod_inv`, `to_signed`)
- `lwe/linalg.py` — matrix × vector helpers
- `lwe/sample.py` — random samplers for matrices/vectors
- `tests/test_keygen.py` — tiny sanity test for keygen
- `docs/` — short math notes
- `data/` — sample instances

## Requirements
- Python 3.10+ (no third‑party packages required)

## Quick start (CLI)
1) Clone the repo and (optionally) create a virtual environment.

2) Key generation — produce a random instance `(A, b, q)` together with the secret `(s, e)` and either print it or save to files.

Print to stdout:
```
python3 main.py keygen -m 5 -n 5 -q 97 -s 42
```
Save to files under `data/` (two files will be produced: `<name>.txt` and `<name>_answere.txt`):
```
python3 main.py keygen -m 5 -n 5 -q 97 -o instance1
```
Notes:
- `-m` rows, `-n` columns for `A`, `-q` modulus, optional `-s/--seed` for RNG seed.
- When `-o name` is provided, files are written to `data/name.txt` and `data/name_answere.txt` (typo in suffix kept for compatibility).

3) Run the demo attack — tries to recover `s` and `e` from the instances in `./data/` whose names match `instance{i}.txt` for `i in [1, 1]` (currently hard‑coded to read `data/instance1.txt`).
```
python3 main.py attack
```
Example output shows the best `L1` score, the recovered `s`, and an estimated error `e`.

## File formats
The generated instance text file looks like this:
```
A=
[ [a11, a12, ..., a1n]
  [a21, a22, ..., a2n]
  ...
  [am1, am2, ..., amn] ]

b=[b1, b2, ..., bm]

q=97
```
- `lwe/reader.py` expects exactly these markers: `A=`, `b=`, and `q=`.
- Whitespace and line breaks inside the matrix block are flexible as long as numbers are intact.

The answer file contains:
```
Answer:
 e = [e1, e2, ..., em]
 s = [s1, s2, ..., sn]
```

## Library usage (Python API)
Key generation:
```python
from lwe.keygen import keygen
import random

rng = random.Random(123)
A, s, e, b = keygen(m=5, n=5, q=97, err_set=[-2,-1,0,1,2], rng=rng)
```
Attack and scoring (self‑contained example using a file instance):
```python
from lwe.attack import solve_lwe, l1_error
from lwe.reader import read_instance

A, b, q = read_instance('data/instance1.txt')
best = solve_lwe(A, b, q=q, trials=200, err_set=[-2,-1,0,1,2])
if best is not None:
    score, s_guess, e_guess = best
    print('L1 score =', score)
    print('s =', s_guess)
    print('e =', e_guess)
else:
    print('No solution found')
```
Reading an instance from a file:
```python
from lwe.reader import read_instance
A, b, q = read_instance('data/instance1.txt')
```

## Status and caveats
- The encryption/decryption modules are present but labeled as WIP and may contain issues. The CLI currently exposes two stable commands: `keygen` and `attack`.
- The demo attack is for small toy sizes only; it is not a real cryptanalytic tool.
- The output answer file uses the suffix `_answere.txt` (original spelling retained).

## Running tests
A tiny test exists for key generation:
```
python3 -m pytest -q
```

## License
This project is licensed under the terms of the LICENSE file included in this repository.
