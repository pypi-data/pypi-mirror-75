from typing import List
import numpy as np
from numba import typed, types, njit, prange

nucleotides_mapping_types = (types.unicode_type, types.int64)


@njit(parallel=True)
def nucleotides_to_numbers(nucleotides: str, sequences: np.ndarray) -> np.ndarray:
    """Return sequences encoded as small integers.

    Parameters
    --------------------------
    nucleotides: str,
        Nucleotides to take in consideration when encoding,
        for instance "acgt".
    sequences: np.ndarray,
        Numpy array with the nucleotide sequences.

    Returns
    --------------------------
    Returns numpy ndarray containing the encoded nucleotides.
    """
    nucleotides_mapping = typed.Dict.empty(*nucleotides_mapping_types)
    for i, n in enumerate(nucleotides):
        nucleotides_mapping[str(n)] = i
        nucleotides_mapping[str(n.upper())] = i

    total_sequences = len(sequences)
    sequence_length = len(sequences[0])

    values = np.empty((total_sequences, sequence_length), dtype=np.int8)
    for i in prange(total_sequences):  # pylint: disable=not-an-iterable
        for j in range(sequence_length):
            nucleotide = str(sequences[i][j])
            if nucleotide in nucleotides_mapping:
                values[i][j] = nucleotides_mapping[nucleotide]
            else:
                values[i][j] = -1

    return values
