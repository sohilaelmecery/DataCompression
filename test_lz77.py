import lz77_compress
import lz77_decompress


def run_test(text):
    tokens = lz77_compress.compress(text)
    result = lz77_decompress.decompress(tokens)

    if result == text:
        print(f"PASS: {text!r}")
        print(f"Tags: {tokens}")
    else:
        print(f"FAIL: {text!r}")
        print(f"Expected: {text!r}")
        print(f"Got:      {result!r}")

    print("-" * 60)


def main():
    test_cases = [
        # Basic text
        "hello world",

        # Repetitive sequences
        "AAAAAA",
        "AAAAAAAAAA",
        "ABABABAB",
        "ABCABCABCABC",

        # Mixed repetition
        "AAAAABAAAAAB",
        "CABRACADABRA",

        # Text with spaces
        "this is a test",

        # Longer repetitive text
        "ABCABCABCABCABCABC",

        # Single character
        "A",

        # Empty string
        "",
    ]

    print("LZ77 Test Cases")
    print("=" * 60)

    for text in test_cases:
        run_test(text)


if __name__ == "__main__":
    main()