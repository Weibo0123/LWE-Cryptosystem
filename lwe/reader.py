"""
reader.py
"""
import re

def parse_matrix(block: str) -> list[list[int]]:
    rows = []
    for line in block.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        nums = re.findall(r'-?\d+', line)
        if nums:
            rows.append(list(map(int, nums)))

    return rows

def parse_vector(text: str) -> list[int]:
    nums = re.findall(r'-?\d+', text)
    return list(map(int, nums))

def read_instance(fname: str) -> tuple[list[list[int]], list[int], int]:
    with open(fname) as f:
        txt = f.read()

    A_block = txt.split("A=")[1].split("b=")[0]
    b_block = txt.split("b=")[1].split("q=")[0]
    q = int(txt.split("q=")[1].strip())

    A = parse_matrix(A_block)
    b = parse_vector(b_block)

    return A, b, q