import sys
import time
import numpy as np


class Decoder:
    table_set_up_time: float
    decoding_table: np.ndarray
    gen_matrix: np.ndarray
    source_words: np.array

    def __init__(self, gen_matrix, source_words):
        # Store generator matrix and source words
        self.gen_matrix = np.array(gen_matrix, dtype=int)
        self.source_words = np.array(source_words, dtype=int)

        # Get number of rows and columns of the generator matrix
        self.n = len(gen_matrix[0])
        self.k = len(gen_matrix)

        # Set up decoding table
        self.decode_rows = 2 ** (self.n - self.k)
        self.decode_cols = 2 ** self.k
        start_time = time.time()
        self.gen_decoding_table()
        stop_time = time.time()
        self.table_set_up_time = stop_time - start_time

    def gen_decoding_table(self):
        # Create empty table
        table = np.zeros((self.decode_rows, self.decode_cols, self.n), dtype=int)

        # Set up representatives
        possible_representatives = self.calc_all_representatives()

        # Calc first row (encoded words)
        table[0] = Decoder.fix_row([np.matmul(word, self.gen_matrix) for word in self.source_words])
        used_representatives = []
        used_representatives.extend(table[0])

        # Calc next rows
        for row in range(1, self.decode_rows):
            representative = Decoder.choose_representative(possible_representatives, used_representatives)
            table[row] = Decoder.fix_row([np.add(representative, cell) for cell in table[0]])
            used_representatives.extend(table[row])

        # Set object decoding table
        self.decoding_table = table

    def calc_all_representatives(self):
        # Get all possible representatives
        unordered = [Decoder.int_to_bin(i, self.n) for i in range(2 ** self.n)]
        # Order them by weight
        ordered = [[] for i in range(self.n + 1)]
        for representative in unordered:
            weight = representative.tolist().count(1)
            ordered[weight].append(representative)
        return ordered

    def decode(self, vector):
        for row in range(self.decode_rows):
            for col in range(self.decode_cols):
                if np.core.array_equal(self.decoding_table[row][col], vector):
                    return self.decoding_table[row][0], self.decoding_table[0][col]
        return None

    def show_decoding_table(self):
        for i in range(self.decode_rows):
            for j in range(self.decode_cols):
                print(self.decoding_table[i][j], end=' ')
            print()

    def show_stats(self):
        print(f"- Time spent generating table:  {self.table_set_up_time} s")
        print(f"- Size occupied by table in RAM: {sys.getsizeof(self.decoding_table)} B")
        print(f"- Table entries: {self.decode_rows * self.decode_cols}")

    def do_tests(self, tests):
        for test in tests:
            vector = np.array(test)
            print("Decoding... ", vector)
            start = time.time()
            decoded = self.decode(vector)
            end = time.time()
            if decoded is None:
                print("Decoding was not possible")
            else:
                print("- Class / Syn-Class: ", decoded[0])
                print("- Word: ", decoded[1])
                print(f"- Time spent decoding: {end - start} s")

    @staticmethod
    def fix_row(row):
        for value in row:
            for bit_index in range(len(value)):
                if value[bit_index] % 2 == 0:
                    value[bit_index] = 0
                else:
                    value[bit_index] = 1
        return row

    @staticmethod
    def int_to_bin(number, n_bits):
        bin_list = [int(x) for x in bin(number)[2:]]
        size = len(bin_list)
        while n_bits > size:
            bin_list.insert(0, 0)
            size += 1
        return np.array(bin_list)

    @staticmethod
    def choose_representative(possible_representatives, used_representatives):
        for weight_list in possible_representatives:
            for candidate in weight_list:
                if next((False for used in used_representatives if np.core.array_equal(used, candidate)), True):
                    used_representatives.append(candidate)
                    return candidate
        return None
