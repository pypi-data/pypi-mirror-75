"""Keras Sequence to lazily one-hot encode sequences from a given bed file."""
from typing import Dict, Tuple, Union
import pandas as pd
import numpy as np
from ucsc_genomes_downloader import Genome
from keras_mixed_sequence import VectorSequence
from .utils import nucleotides_to_numbers, fast_to_categorical


class BedSequence(VectorSequence):
    """Keras Sequence to lazily one-hot encode sequences from a given bed file."""

    def __init__(
        self,
        assembly: Genome,
        bed: pd.DataFrame,
        batch_size: int,
        nucleotides: str = "actg",
        unknown_nucleotide_value: float = 0.25,
        seed: int = 42,
        elapsed_epochs: int = 0,
        shuffle: bool = True
    ):
        """Return new BedSequence object.

        Parameters
        --------------------
        assembly: Genome,
            Genomic assembly from ucsc from which to extract sequences.
        bed: pd.DataFrame,
            Pandas DataFrame containing minimal bed columns,
            like "chrom", "chromStart" and "chromEnd".
        batch_size: int,
            Batch size to be returned for each request.
        nucleotides: str = "actg",
            Nucleotides to consider when one-hot encoding.
        unknown_nucleotide_value: float = 0.25,
            The default value to use for encoding unknown nucleotides.
        seed: int = 42,
            Starting seed to use if shuffling the dataset.
        elapsed_epochs: int = 0,
            Number of elapsed epochs to init state of generator.
        shuffle: bool = True,
            Wethever to shuffle or not the sequence.

        Raises
        --------------------
        ValueError:
            If the bed file regions does not have the same length.
        """
        # Every window in the bed file must be
        # of the same length.
        if len(set((bed.chromEnd - bed.chromStart).values)) != 1:
            raise ValueError(
                "The bed file regions must have the same length!"
            )

        self._window_length = (bed.chromEnd - bed.chromStart).values[0]
        self._genome = assembly
        self._nucleotides = nucleotides
        self._nucleotides_number = len(nucleotides)
        self._unknown_nucleotide_value = unknown_nucleotide_value

        # We extract the sequences of the bed file from
        # the given genome.
        sequences = np.array(self._genome.bed_to_sequence(bed), dtype=str)

        super().__init__(
            nucleotides_to_numbers(self.nucleotides, sequences),
            batch_size,
            seed=seed,
            elapsed_epochs=elapsed_epochs,
            shuffle=shuffle
        )

    @property
    def window_length(self) -> int:
        """Return number of nucleotides in a window."""
        return self._window_length

    @property
    def nucleotides(self) -> int:
        """Return number of nucleotides considered."""
        return self._nucleotides

    @property
    def nucleotides_number(self) -> int:
        """Return number of nucleotides considered."""
        return self._nucleotides_number

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """Return batch corresponding to given index.

        Parameters
        ---------------
        idx: int,
            Index corresponding to batch to be rendered.

        Returns
        ---------------
        Return Tuple containing X and Y numpy arrays corresponding to given batch index.
        """
        return fast_to_categorical(
            super().__getitem__(idx),
            num_classes=self.nucleotides_number,
            unknown_nucleotide_value=self._unknown_nucleotide_value
        )
