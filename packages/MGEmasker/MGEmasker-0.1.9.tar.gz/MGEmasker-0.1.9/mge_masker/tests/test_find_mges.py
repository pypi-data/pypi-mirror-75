import pytest
import os
import inspect
import tempfile
from collections import OrderedDict
from mge_masker.mge_masker_functions import find_mges, merge_mges, create_mge_gff_file

@pytest.fixture(scope="module")
def test_genome_file_path():
  test_genome_file_path = os.path.realpath(
    os.path.abspath(
      os.path.join(
        os.path.split(inspect.getfile( inspect.currentframe() ))[0],
        "data",
        "test.gbk"
      )
    )
  )
  return(test_genome_file_path)

@pytest.fixture(scope="module")
def expected_gff_file_path():
  expected_gff_file_path = os.path.realpath(
    os.path.abspath(
      os.path.join(
        os.path.split(inspect.getfile( inspect.currentframe() ))[0],
        "data",
        "test.gff"
      )
    )
  )
  return(expected_gff_file_path)

@pytest.fixture(scope="module")
def expected_mges():
  return (
    [
      {'type': 'CDS', 'start': 201, 'end': 400, 'strand': '+', 'description': OrderedDict([('note', ['Possible transposase based on homology'])])},
      {'type': 'CDS', 'start': 401, 'end': 500, 'strand': '-', 'description': OrderedDict([('product', ['Phage protein'])])},
      {'type': 'CDS', 'start': 501, 'end': 600, 'strand': '+', 'description': OrderedDict([('product', ['IS101'])])},
      {'type': 'CDS', 'start': 701, 'end': 800, 'strand': '+', 'description': OrderedDict([('product', ['Integrase'])])}
    ]
  )

@pytest.fixture(scope="module")
def test_mges_for_merging():
  return (
    [
      {'type': 'CDS', 'start': 1000, 'end': 2000, 'strand': '+', 'description': OrderedDict([('note', ['Possible transposase based on homology'])])},
      {'type': 'CDS', 'start': 2500, 'end': 3500, 'strand': '-', 'description': OrderedDict([('product', ['Phage protein'])])},
      {'type': 'CDS', 'start': 5000, 'end': 6000, 'strand': '+', 'description': OrderedDict([('product', ['IS101'])])},
      {'type': 'CDS', 'start': 7000, 'end': 8000, 'strand': '+', 'description': OrderedDict([('product', ['Integrase'])])},
      {'type': 'CDS', 'start': 8500, 'end': 9000, 'strand': '+', 'description': OrderedDict([('product', ['Repeat'])])},
      {'type': 'CDS', 'start': 12000, 'end': 13000, 'strand': '-', 'description': OrderedDict([('product', ['Tandem repeat'])])}
    ]
  )

@pytest.fixture(scope="module") 
def expected_mges_after_merging_1000_interval():
  return (
    [
      {
        'type': '2 merged features',
        'start': 1000, 'end': 3500, 'strand': '.',
        'description': OrderedDict([('note', ['Possible transposase based on homology']), ('product', ['Phage protein'])])
      },
      {
        'type': '3 merged features',
        'start': 5000, 'end': 9000, 'strand': '+',
        'description': OrderedDict([('product', ['IS101', 'Integrase', 'Repeat'])])
      },
      {
        'type': 'CDS', 
        'start': 12000, 'end': 13000, 'strand': '-',
        'description': OrderedDict([('product', ['Tandem repeat'])])
      }
    ]
  )
@pytest.fixture(scope="module") 
def expected_mges_after_merging_500_interval():
  return (
    [
      {
        'type': '2 merged features',
        'start': 1000, 'end': 3500, 'strand': '.',
        'description': OrderedDict([('note', ['Possible transposase based on homology']), ('product', ['Phage protein'])])
      },
      {'type': 'CDS', 'start': 5000, 'end': 6000, 'strand': '+', 'description': OrderedDict([('product', ['IS101'])])},
      {
        'type': '2 merged features',
        'start': 7000, 'end': 9000, 'strand': '+',
        'description': OrderedDict([('product', ['Integrase', 'Repeat'])])
      },
      {
        'type': 'CDS', 
        'start': 12000, 'end': 13000, 'strand': '-',
        'description': OrderedDict([('product', ['Tandem repeat'])])
      }
    ]
  )
  
def test_find_mges(test_genome_file_path, expected_mges):
  mges = find_mges(test_genome_file_path, "genbank")
  
  for index, mge in enumerate(mges):
    assert mge == expected_mges[index]


def test_merge_mges_500_interval(test_mges_for_merging, expected_mges_after_merging_500_interval):
  merged_mges = merge_mges(test_mges_for_merging, 500)
  for index, mge in enumerate(merged_mges):
    assert mge == expected_mges_after_merging_500_interval[index]

def test_merge_mges_1000_interval(test_mges_for_merging, expected_mges_after_merging_1000_interval):
  merged_mges = merge_mges(test_mges_for_merging, 1000)
  for index, mge in enumerate(merged_mges):
    assert mge == expected_mges_after_merging_1000_interval[index]
    
def test_create_file(test_genome_file_path, expected_gff_file_path):
  with tempfile.NamedTemporaryFile(mode = "w") as temp_genome:
    with open(test_genome_file_path) as test_genome_file:
      genome_string = test_genome_file.read()
    temp_genome.write(genome_string)
    temp_genome.flush()
    mges = find_mges(temp_genome.name, "genbank")
    gff_file_path = create_mge_gff_file(temp_genome.name, "genbank", mges)
    with open(gff_file_path) as gff_file:
      gff_string = gff_file.read()
    with open(expected_gff_file_path) as expected_gff_file:
      expected_gff_string = expected_gff_file.read()
    assert gff_string == expected_gff_string
      

