from Bio import SeqIO
from Bio import AlignIO
from Bio.Alphabet import generic_dna 
from Bio.Seq import Seq 
from Bio.SeqRecord import SeqRecord 
from Bio.Align import MultipleSeqAlignment 
import inspect
import copy
import sys
import os
import re
from pathlib import Path
import csv
from collections import OrderedDict


def get_mge_patterns(mge_file_path = None):
  # read text file with pattern match regular expressions and return a list of compiled regexs
  if not mge_file_path:
    mge_file_path = os.path.join(os.path.dirname(__file__), "mge_patterns.txt")
  mge_patterns = []
  with open(mge_file_path) as mge_file:
    for line in mge_file.readlines():
      pattern = re.compile(line.rstrip())
      mge_patterns.append(pattern)
  return(mge_patterns)

def get_features(genome_file_path, file_format):
  record = SeqIO.read(genome_file_path, file_format)
  return(record.features)

def create_gff_line(accession, mge):
  description = mge['description']
  description_string = ';'.join([f'{match}="{",".join(description[match])}"' for match in description])
  return(f'{accession}\t.\t{mge["type"]}\t{mge["start"]}\t{mge["end"]}\t.\t{mge["strand"]}\t.\t{description_string}\n')

def search_features_for_patterns(features, mge_patterns):
  mges = []
  for feature in features:
    qualifiers = OrderedDict()
    for qualifier in feature.qualifiers:
      if qualifier in ['product','note']:
          qualifiers[qualifier] = feature.qualifiers[qualifier]
    if len(qualifiers) > 0:
      matches = OrderedDict()
      for qualifier in qualifiers:
        for qualifier_value in qualifiers[qualifier]:
          for pattern in mge_patterns:
            if pattern.match(qualifier_value):
              if qualifier not in matches:
                matches[qualifier] = []
              matches[qualifier].append(qualifier_value)
      if len(matches) > 0:
        if feature.strand:
          if feature.strand == 1:
            strand = "+"
          elif feature.strand == -1:
            strand = "-"
        else:
          strand = "."
        mges.append(
          {
            "type": feature.type,
            "start": feature.location.start.position + 1,
            "end": feature.location.end.position,
            "strand": strand,
            "description": matches
          }
        )
  return(mges)

def find_mges(genome_file_path, file_format, mge_file_path = None):
  """
  returns mges as a list of dicts with the keys: type, start, end, strand, description
  """
  features = get_features(genome_file_path, file_format)
  mge_patterns = get_mge_patterns(mge_file_path)
  mges = search_features_for_patterns(features, mge_patterns)
  return(mges)


def merge_mges(mges, merge_interval):
  previous_mge = {}
  merged_mge = { "type": None, "start": None, "end": None, "strand": None, "description": {}}
  number_mges_merged = 1
  merged_mges = []
  for mge in mges:
    if not previous_mge:
      previous_mge = mge
    else:
      # check if this mge should be merged with previous
      if mge['start'] - previous_mge['end'] <= merge_interval: # merge if less than interval
        if not merged_mge['start']:
          merged_mge['start'] = previous_mge['start']
        merged_mge['end'] = mge['end']
        if not merged_mge['strand']:
          merged_mge['strand'] = previous_mge['strand']
        if mge['strand'] != merged_mge['strand']:
            merged_mge['strand'] = '.'

        if not merged_mge['description']:
          merged_mge['description'] = copy.deepcopy(previous_mge['description'])
        # merge the descriptions
        for match in mge['description']:
          if match not in merged_mge['description']:
            merged_mge['description'][match] = []
          merged_mge['description'][match].extend(mge['description'][match])
        number_mges_merged += 1
      else:
        # check if a mge has been merged
        if merged_mge['start']:
          merged_mge['type'] = f"{number_mges_merged} merged features"
          merged_mges.append(merged_mge)
          # reset merged_mge
          merged_mge = { "type": None, "start": None, "end": None, "strand": None, "description": {}}
          number_mges_merged = 1
        else:
          merged_mges.append(previous_mge)
      previous_mge = mge
    
    # Final merge
  if merged_mge['start']:
    merged_mge['type'] = f"{number_mges_merged} merged features"
    merged_mges.append(merged_mge)
    # reset merged_mge
    merged_mge = { "type": None, "start": None, "end": None, "strand": None, "description": {}}
  else:
    merged_mges.append(previous_mge)

  return(merged_mges)
        

def create_mge_gff_file(genome_file_path, file_format, mges):
  record = SeqIO.read(genome_file_path, file_format)
  gff_file_path = Path(genome_file_path).with_suffix('.gff')
  with open(gff_file_path, "w") as gff_file:
    for mge in mges:
      gff_file.write(create_gff_line(record.name, mge))
  return(gff_file_path)

def extract_position_ranges_from_gff_file(gff_file_path):
  with open(gff_file_path) as gff_file:
    reader = csv.reader(gff_file, delimiter='\t')
    start_and_end_positions = [(int(row[3]), int(row[4])) for row in reader]
  return(start_and_end_positions)

def find_min_and_max_positions(positions):
  min_pos = min([pos[0] for pos in positions])
  max_pos= max([pos[1] for pos in positions])
  return(min_pos, max_pos)

def check_alignment(alignment, gff_ranges):
  # get alignment length
  alignment_length = alignment.get_alignment_length()
  # get max position specified in the GFF file
  min_pos, max_pos = find_min_and_max_positions(gff_ranges)
  # check max pos doesn't exceed alignment length
  if alignment_length < max_pos:
    sys.exit(f'The maximum position {max_pos} specified in the GFF file exceeds the alignment length')
  

def mask_mges(pseudogenome_alignment_path, gff_file_path, masking_character):
  alignment = AlignIO.read(pseudogenome_alignment_path, 'fasta')
  gff_ranges = extract_position_ranges_from_gff_file(gff_file_path)
  check_alignment(alignment, gff_ranges)

  masked_sequences = []
  for index, record in enumerate(alignment):
    if index+1 > 0 and (index+1) % 10 == 0:
      print(f'Masking sequence {index+1}')
    sequence = record.seq
    for gff_range in gff_ranges:
      start = gff_range[0] -1
      end = gff_range[1]
      difference = end - start
      sequence = f'{sequence[:start]}{masking_character*difference}{sequence  [end:]}'
    masked_sequences.append(SeqRecord(Seq(sequence, generic_dna), id=record.id, description = ""))
    
  masked_alignment = MultipleSeqAlignment(masked_sequences)
  masked_pseudogenome_alignment_path = Path(pseudogenome_alignment_path).with_suffix('.masked.fas')  
  with open(masked_pseudogenome_alignment_path, "w") as masked_pseudogenome_alignment:
    masked_pseudogenome_alignment.write(masked_alignment.format('fasta'))
  return(masked_pseudogenome_alignment_path)
  

def print_default_regex_patterns():
  mge_file_path = os.path.join(os.path.dirname(__file__), "mge_patterns.txt")
  with open(mge_file_path) as mge_file:
    for line in mge_file.readlines():
      print(line.rstrip())


  