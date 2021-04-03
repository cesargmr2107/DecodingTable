import sys

from Decoder import Decoder
from SyndromeDecoder import SyndromeDecoder


def general_test(test_name, decoder_class, source_words, gen_matrix, parity_control_matrix, tests):
    print("\n" + "-" * 100 + "\n")
    print(f"{test_name}")
    print("\n" + "-" * 100 + "\n")

    if decoder_class is Decoder:
        decoder = Decoder(gen_matrix, source_words)
    else:
        decoder = SyndromeDecoder(gen_matrix, source_words, parity_control_matrix)
    print("Code source words:\n", decoder.source_words, "\n")
    print("Code generator matrix:\n", decoder.gen_matrix, "\n")
    if decoder_class is SyndromeDecoder:
        print("Parity control matrix:\n", decoder.parity_control_matrix, "\n")
    print("Generated decoding table:")
    decoder.show_decoding_table()
    print("\nDecoder Stats:")
    decoder.show_stats()
    print("\nTesting decoding process:\n")
    decoder.do_tests(tests)
    print("\n" + "-" * 100)


def test(decoder_class):
    # Configure output
    filename = f"test_{decoder_class.__name__}_output.txt"
    sys.stdout = open(filename, 'w')

    # Do tests
    print("=" * 100)
    print(f"\nTESTING '{decoder_class.__name__}'")

    source_words = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]

    # Do test for 2.4.4 example

    general_test(
        decoder_class=decoder_class,
        test_name="2.4.4. TESTING TRIPLE PARITY CODE",
        source_words=source_words,
        gen_matrix=[
            [1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1]
        ],
        parity_control_matrix=[
            [1, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 1]
        ],
        tests=[
            [1, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 1]
        ]
    )

    # Do test for 2.4.5 example

    general_test(
        decoder_class=decoder_class,
        test_name="2.4.5. TESTING (5,3)-LINEAL CODE",
        source_words=source_words,
        gen_matrix=[
            [1, 0, 0, 1, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1]
        ],
        parity_control_matrix=[
            [1, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]
        ],
        tests=[
            [0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 0, 0]
        ]
    )

    sys.stdout.close()
