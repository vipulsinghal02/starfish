"""
Tests for codebook.synthetic_one_hot_codebook method
"""

import numpy as np
import pytest

from starfish import Codebook
from starfish.types import Features, Indices


def test_synthetic_one_hot_codebook_returns_requested_codebook():
    """
    Make a request and verify that the size and shape match the request, and
    that each round has only one round 'on'.
    """
    codebook: Codebook = Codebook.synthetic_one_hot_codebook(
        n_round=4,
        n_channel=2,
        n_codes=3
    )

    assert codebook.sizes == {Indices.CH: 2, Indices.ROUND: 4, Features.TARGET: 3}
    assert np.all(codebook.sum(Indices.CH.value) == 1), "the numbers of channels on per round != 1"


def test_target_names_are_incorporated_into_synthetic_codebook():
    """Verify that target names are incorporated in order."""
    codebook: Codebook = Codebook.synthetic_one_hot_codebook(
        n_round=3,
        n_channel=6,
        n_codes=2,
        target_names=list('ab'),
    )

    assert np.array_equal(codebook[Features.TARGET], list('ab'))


# TODO ambrosejcarr: This should probably be clearer than an AssertionError
def test_wrong_number_of_target_names_raises_error():
    """here we request 3 codes but provide only two names, which should raise an error"""
    with pytest.raises(AssertionError):
        Codebook.synthetic_one_hot_codebook(
            n_round=2,
            n_channel=2,
            n_codes=3,
            target_names=list('ab')
        )
