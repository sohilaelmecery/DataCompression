"""
LZ77 COMPRESSOR  (follows Lecture 1: tag = <Position, Length, Next Symbol>)

  Position    : how many steps BACK from the start of the look-ahead buffer
                the longest match begins (0 when there is no match)
  Length      : length of the longest match
                (may be > Position -> overlapping match, which handles
                 repetitive sequences like "BBBBBBBBBB" or "ABABABAB")

  Next Symbol : the symbol right after the match
                (None = NULL when the match reaches the end of the input)

If several matches have the same length, the CLOSEST one is used
(this is what the lecture examples do, e.g. <2,1,"D"> in the CABRACADABRA example).

Usage:
  python lz77_compress.py                      (interactive)
  python lz77_compress.py input.txt [out.json] (file mode, default out: tokens.json)
"""

import json
import sys


def compress(data, window_size=4096, lookahead_size=255):
    """Return a list of (position, length, next_symbol) tags."""
    tokens = []
    n = len(data)
    i = 0

    while i < n:
        best_len = 0
        best_pos = 0

        start = max(0, i - window_size)
        max_len = min(lookahead_size, n - i)

        # Go from the CLOSEST candidate to the farthest; only a strictly
        # longer match replaces the current best (so ties keep the closest).
        for j in range(i - 1, start - 1, -1):
            length = 0
            # data[j + length] may run past i: this is the overlapping case.
            while length < max_len and data[j + length] == data[i + length]:
                length += 1
            if length > best_len:
                best_len = length
                best_pos = i - j

        if i + best_len < n:
            next_symbol = data[i + best_len]
        else:
            next_symbol = None  # NULL: the match reached the end of the input

        tokens.append((best_pos, best_len, next_symbol))

        if next_symbol is None:
            i += best_len
        else:
            i += best_len + 1

    return tokens


def compression_stats(data, tokens, symbol_bits=8):
    """Compression ratio exactly like the lecture:
       bits(Position) = bits needed for max Position
       bits(Length)   = bits needed for max Length
       bits(Symbol)   = symbol_bits (8 for ASCII)
    """
    if not tokens:
        return {"original_bits": 0, "compressed_bits": 0, "ratio": 0}

    pos_bits = max(1, max(t[0] for t in tokens).bit_length())
    len_bits = max(1, max(t[1] for t in tokens).bit_length())
    tag_bits = pos_bits + len_bits + symbol_bits

    original = len(data) * symbol_bits
    compressed = len(tokens) * tag_bits
    return {
        "original_bits": original,
        "position_bits": pos_bits,
        "length_bits": len_bits,
        "tag_bits": tag_bits,
        "num_tags": len(tokens),
        "compressed_bits": compressed,
        "ratio": compressed / original,
    }


def save_tokens(tokens, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        out_path = sys.argv[2] if len(sys.argv) >= 3 else "tokens.json"
    else:
        text = input("Enter text to compress: ")
        out_path = "tokens.json"

    tokens = compress(text)
    save_tokens(tokens, out_path)

    print("Tags:", tokens)
    s = compression_stats(text, tokens)
    print(f"Original size  : {s['original_bits']} bits")
    print(f"Tag size       : {s['position_bits']} + {s['length_bits']} + 8 = {s['tag_bits']} bits")
    print(f"Number of tags : {s['num_tags']}")
    print(f"Compressed size: {s['compressed_bits']} bits")
    print(f"Ratio          : {s['ratio']:.3f}")
    print(f"Saved to {out_path}")