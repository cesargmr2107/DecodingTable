import numpy as np
from Decoder import Decoder


class SyndromeDecoder(Decoder):
    decoding_table: dict
    parity_control_matrix: np.ndarray

    def __init__(self, gen_matrix, source_words, parity_control_matrix):
        self.parity_control_matrix = np.array(parity_control_matrix)
        super().__init__(gen_matrix, source_words)
        self.decode_cols = 2

    def gen_decoding_table(self):
        # Create empty table
        table = {}

        # Set up representatives
        possible_representatives = super().calc_all_representatives()
        used_syndromes = []

        # Calc syndromes
        for row in range(self.decode_rows):
            (repr, syndrome) = self.choose_representative(possible_representatives, used_syndromes)
            table[np.array_str(syndrome)] = repr

            used_syndromes.append(syndrome)

        # Set object decoding table
        self.decoding_table = table

    def calc_syndrome(self, vector: np.ndarray):
        pc_transpose = np.transpose(self.parity_control_matrix)
        return Decoder.fix_row([np.matmul(vector, pc_transpose)])[0]

    def choose_representative(self, possible_representatives, used_syndromes):
        for weight_list in possible_representatives:
            for candidate in weight_list:
                candidate_syndrome = self.calc_syndrome(candidate)
                if next((False for used in used_syndromes if np.core.array_equal(used, candidate_syndrome)), True):
                    used_syndromes.append(candidate_syndrome)
                    return candidate, candidate_syndrome
        return None

    def decode(self, vector):
        syndrome = self.calc_syndrome(vector)
        representative = self.decoding_table[np.array_str(syndrome)]
        return f"{syndrome}-{representative}", Decoder.fix_row([np.add(vector, representative)])[0]

    def show_decoding_table(self):
        for (representative, syndrome) in self.decoding_table.items():
            print(f"{representative} {syndrome}")
