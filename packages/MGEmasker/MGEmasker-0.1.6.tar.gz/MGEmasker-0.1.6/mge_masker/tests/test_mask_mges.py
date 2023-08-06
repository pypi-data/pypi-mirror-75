import pytest
import os
import inspect
import tempfile
from collections import OrderedDict
from mge_masker.mge_masker_functions import extract_position_ranges_from_gff_file, find_min_and_max_positions, mask_mges

@pytest.fixture(scope="module")
def test_gff_file_path():
  gff_file_path = os.path.realpath(
    os.path.abspath(
      os.path.join(
        os.path.split(inspect.getfile( inspect.currentframe() ))[0],
        "data",
        "test.gff"
      )
    )
  )
  return(gff_file_path)

@pytest.fixture(scope="module")
def test_alignment_file_path():
  alignment_file_path = os.path.realpath(
    os.path.abspath(
      os.path.join(
        os.path.split(inspect.getfile( inspect.currentframe() ))[0],
        "data",
        "test_alignment.fas"
      )
    )
  )
  return(alignment_file_path)

@pytest.fixture(scope="module")
def test_masked_alignment_file_path():
  masked_alignment_file_path = os.path.realpath(
    os.path.abspath(
      os.path.join(
        os.path.split(inspect.getfile( inspect.currentframe() ))[0],
        "data",
        "test_alignment.masked.fas"
      )
    )
  )
  return(masked_alignment_file_path)


def test_extract_boundaries_from_gff_file(test_gff_file_path):
  start_and_end_positions = extract_position_ranges_from_gff_file(test_gff_file_path)
  
  assert start_and_end_positions == [(201,400), (401,500), (501,600), (701,800)]


def test_extract_position_ranges_from_gff_file(test_gff_file_path):
  start_and_end_positions = extract_position_ranges_from_gff_file(test_gff_file_path)
  min, max = find_min_and_max_positions(start_and_end_positions)
  assert min == 201
  assert max == 800
  
def test_mask_mges(test_alignment_file_path, test_masked_alignment_file_path, test_gff_file_path):
  with tempfile.NamedTemporaryFile(mode = "w") as temp_alignment:
    with open(test_alignment_file_path) as test_alignment_file:
      alignment_string = test_alignment_file.read()
    temp_alignment.write(alignment_string)
    temp_alignment.flush()
    masked_pseudogenome_alignment_path= mask_mges(temp_alignment.name, test_gff_file_path, "N")
    with open(masked_pseudogenome_alignment_path) as masked_pseudogenome_alignment:
      masked_alignment_string = masked_pseudogenome_alignment.read()
    with open(test_masked_alignment_file_path) as test_masked_alignment_file:
      expected_masked_alignment_string = test_masked_alignment_file.read()
    assert masked_alignment_string == expected_masked_alignment_string
    

