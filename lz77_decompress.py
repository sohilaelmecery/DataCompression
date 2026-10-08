"""
LZ77 DECOMPRESSOR

Reads the tags produced by lz77_compress.py and rebuilds the original text.
A next symbol of None (NULL) means "nothing to append after the copy".

Usage:
  python lz77_decompress.py                          (reads tokens.json)
  python lz77_decompress.py tokens.json [out.txt]    (optionally write result to file)
"""

import json
import sys


def decompress(tokens):
    """Rebuild the original string from (position, length, next_symbol) tags."""
    out = []
    for position, length, next_symbol in tokens:
        start = len(out) - position
        for k in range(length):
            # Copy ONE symbol at a time (not a slice) so overlapping
            # matches work: we may copy symbols we just wrote.
            out.append(out[start + k])
        if next_symbol is not None:
            out.append(next_symbol)
    return "".join(out)


def load_tokens(path):
    with open(path, "r", encoding="utf-8") as f:
        return [tuple(t) for t in json.load(f)]


if __name__ == "__main__":
    in_path = sys.argv[1] if len(sys.argv) >= 2 else "tokens.json"
    tokens = load_tokens(in_path)
    text = decompress(tokens)

    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Decompressed text written to {sys.argv[2]}")
    else:
        print("Decompressed:", text)
