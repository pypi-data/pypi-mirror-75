#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `utils` module."""

import pytest  # noqa: F401
import read_structure_step  # noqa: F401
from . import build_filenames


@pytest.mark.parametrize("file_name", ["spc.xyz", "spc"])
@pytest.mark.parametrize("extension", [None, ".xyz", "xyz", "XYZ", "xYz"])
def test_extensions(file_name, extension):

    xyz_file = build_filenames.build_data_filename(file_name)
    parsed_xyz = read_structure_step.read(xyz_file, extension=extension)

    assert len(parsed_xyz["atoms"]["elements"]) == 3
    assert all(
        atom in ["O", "H", "H"] for atom in parsed_xyz["atoms"]["elements"]
    )
    assert len(parsed_xyz["atoms"]["coordinates"]) == 3
    assert all(len(point) == 3 for point in parsed_xyz["atoms"]["coordinates"])
    assert len(parsed_xyz["bonds"]) == 2
    assert any(
        set(bond) == set((2, 1, 'single')) for bond in parsed_xyz["bonds"]
    )
    assert any(
        set(bond) == set((3, 1, 'single')) for bond in parsed_xyz["bonds"]
    )


def test_sanitize_file_format_regex_validation():

    with pytest.raises(NameError):
        read_structure_step.read("spc.xyz", extension=".xy-z")
