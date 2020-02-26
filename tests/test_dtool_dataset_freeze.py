"""Test the ``dtool dataset create`` command."""

import os

from click.testing import CliRunner

from dtoolcore import DataSet, ProtoDataSet
from dtoolcore.utils import sanitise_uri

from . import chdir_fixture, tmp_dir_fixture  # NOQA


def test_dataset_freeze_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create, freeze, add
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    # At this point we have a proto dataset
    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = sanitise_uri(dataset_abspath)
    dataset = ProtoDataSet.from_uri(dataset_uri)

    # Create sample file to the proto dataset.
    sample_file_name = "hello.txt"
    with open(sample_file_name, "w") as fh:
        fh.write("hello world")

    # Put it into the dataset

    result = runner.invoke(add, ["item", sample_file_name, dataset_uri])
    assert result.exit_code == 0

    result = runner.invoke(freeze, [dataset_uri])
    assert result.exit_code == 0

    # Now we have a dataset.
    dataset = DataSet.from_uri(dataset_uri)

    # Manifest has been updated.
    assert len(dataset.identifiers) == 1


def test_dataset_freeze_rogue_content_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create, freeze
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    # At this point we have a proto dataset
    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = sanitise_uri(dataset_abspath)

    # Create rogue data file
    sample_file_name = os.path.join(dataset_abspath, "hello.txt")
    with open(sample_file_name, "w") as fh:
        fh.write("hello world")

    result = runner.invoke(freeze, [dataset_uri])
    assert result.exit_code == 4
    assert result.output.find("Rogue content") != -1
