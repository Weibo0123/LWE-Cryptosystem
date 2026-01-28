# LWE-Cryptosystem

## Mathematical Conventions

- Modulus: all arithmetic is performed modulo q.


- Dimensions:
  - $A \in \mathbb{Z}_q^{m \times n}$
  - $s \in \mathbb{Z}_q^{n}$
  - $e \in \text{small}^m$
  - $b = As + e \pmod q$, so $b \in \mathbb{Z}_q^{m}$


- Encryption:
  - $r \in \{0,1\}^m$
  - $u = r^T A \in \mathbb{Z}_q^n$
  - $v = r^T b + \text{bit}\cdot \lfloor q/2 \rfloor \pmod q$

Feel confused about the symbols?

Don't worry! Check [docs/mathematical_conventions.md](docs/mathematical_conventions.md) for more explanation.
