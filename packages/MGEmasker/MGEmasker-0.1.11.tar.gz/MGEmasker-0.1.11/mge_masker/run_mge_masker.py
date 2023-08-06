#!/usr/bin/env python3
import argparse
import sys
import os
import textwrap
from mge_masker.mge_masker_functions import find_mges, create_mge_gff_file, mask_mges, merge_mges, print_default_regex_patterns

def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg


def parse_args():
    description = textwrap.dedent(
        """
        A module to find MGEs in a rich sequence file and mask regions corresponding to the MGEs in a pseudogenome alignment.
        
        The find_mges command searches a gbk or embl file for features that have MGE-associated annotations.
        It writes a GFF file containing the positions of the matched features.
        
        The mask_mges command takes a GFF file produced using the find_mges command and masks those regions in all sequences of a pseudogenome alignment based on the reference sequence used to find MGEs.
        """
    )

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(
        help='The following commands are available. Type mge_masker <COMMAND> -h for more help on a specific commands',
        dest='command'
    )

    subparsers.required = True

    find_mges = subparsers.add_parser('find_mges',
        help='Search a rich sequence file for features annotated with text that suggests a MGE-associated element'
    )

    find_mges.add_argument('-g', '--genome_file_path', type=lambda x: is_valid_file(parser, x), help='path to a genome file', required=True)
    find_mges.add_argument('-f', '--file_format',
                        help='genome file format',
                        default = 'genbank',
                        choices=['genbank', 'embl']
                        )
    find_mges.add_argument('-i', '--merge_interval', help='The maximum distance between MGEs when performing the merging step (Default 1000bp)', default=1000, type = int)
    find_mges.add_argument('-m', '--mge_file_path', type=lambda x: is_valid_file(parser, x), help='path to a file containing regex MGE annotations')
    
    mask_mges = subparsers.add_parser('mask_mges',
        help='Mask regions from a pseudogenome alignment with the regions in a GFF file produced using the find_mges command'
    )
    mask_mges.add_argument('-f', '--fasta_path', help='path to either a single fasta reference or a pseudogenome alignment file', type=lambda x: is_valid_file(parser, x), required=True)
    mask_mges.add_argument('-g', '--gff_file_path', help='path to a gff file containing MGE regions to be masked', type=lambda x: is_valid_file(parser, x), required=True)
    mask_mges.add_argument('-m', '--masking_character', help='character used to mask (default: N)', default='N')
    
    default_matches = subparsers.add_parser('default_matches',
        help='Show the default regex patterns used when searching for MGEs'
    )
    
    return(parser.parse_args())





def main():
    options = parse_args()
    if (options.command == 'find_mges'):
        mges = find_mges(options.genome_file_path, options.file_format, options.mge_file_path)
        print(f'Found {len(mges)} MGEs')
        merged_mges = merge_mges(mges, options.merge_interval)
        if len(merged_mges) < len(mges):
            print(f'{len(mges)} MGEs were merged into {len(merged_mges)}')
        else:
            print('No MGEs were merged')
        gff_file_path = create_mge_gff_file(options.genome_file_path, options.file_format, merged_mges)
        print(f'GFF file written to {gff_file_path}')
    elif (options.command == 'mask_mges'):
        masked_alignment_file_path = mask_mges(options.fasta_path, options.gff_file_path, options.masking_character)
        print(f'Masked alignment file written to {masked_alignment_file_path}')
    elif(options.command == 'default_matches'):
        print_default_regex_patterns()
    
 

if __name__ == "__main__":
    main()

