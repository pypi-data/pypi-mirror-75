import numpy as np
from numba import njit, prange


@njit(parallel=True)
def fast_to_categorical(y: np.ndarray, num_classes: int, unknown_nucleotide_value: float) -> np.ndarray:
    """Return one hot encoded batches.

    This is our implementation of to_categorical from keras.
    This implementation runs 6 times faster.

    Parameters
    -----------------
    y:np.np.ndarray,
        Vector of the batches. This vector has shape (batch_size, window_len)
    num_classes: int,
        Number of classes to one-hot encode.
    unknown_nucleotide_value: float
        Value to use for the unkown nucleotide class.

    Returns
    -----------------
    One hot encoded batches.
    """
    batch_size, window_length = y.shape
    zeros = np.zeros(
        shape=(batch_size, window_length, num_classes),
        dtype=np.float_
    )
    for i in prange(batch_size):  # pylint: disable=not-an-iterable
        for j in range(window_length):
            class_number = y[i][j]
            if class_number < 0:
                for k in range(num_classes):
                    zeros[i][j][k] = unknown_nucleotide_value
            else:
                zeros[i][j][class_number] = 1
    return zeros
