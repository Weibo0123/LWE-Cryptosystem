"""
encoding.py
"""

def text_to_bits(s: str) -> list[int]:
    data = s.encode("utf-8")
    bits = []

    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def bits_to_text(bits: list[int]) -> str:
    if len(bits) % 8 != 0:
        raise ValueError("bit length must be multiple of 8")
    out = bytearray()
    for k in range(0, len(bits), 8):
        byte = 0
        for i in range(8):
            byte = (byte << 1) | (bits[k + i] & 1)
        out.append(byte)
    return out.decode("utf-8", errors="strict")
