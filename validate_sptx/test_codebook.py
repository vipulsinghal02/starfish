import pytest
from pkg_resources import resource_filename

from .util import SpaceTxValidator

codebook_schema_path = resource_filename("validate_sptx", "schema/codebook/codebook.json")
validator = SpaceTxValidator(codebook_schema_path)


def test_codebook():
    codebook_example_path = resource_filename(
        "validate_sptx", "examples/codebook/codebook.json")
    assert validator.validate_file(codebook_example_path)


def test_diagonal_codebook():
    codebook_example_path = resource_filename(
        "validate_sptx", "examples/codebook/codebook_diagonal.json")
    assert validator.validate_file(codebook_example_path)


def test_diagonal_codebook_full_values():
    codebook_example_path = resource_filename(
        "validate_sptx", "examples/codebook/codebook_diagonal_inferred_value.json")
    assert validator.validate_file(codebook_example_path)


def test_codebook_missing_channel_raises_validation_error():
    codebook_example_path = resource_filename(
        "validate_sptx", "examples/codebook/codebook.json")
    codebook = validator.load_json(codebook_example_path)
    del codebook[0]['codeword'][0]['c']
    with pytest.warns(UserWarning):
        assert not validator.validate_object(codebook)
